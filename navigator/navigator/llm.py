# SPDX-License-Identifier: Apache-2.0
"""Pluggable model client. Three backends:

  - 'ollama' : a local/LAN Ollama server
  - 'openai' : any OpenAI-compatible endpoint (key via NAVIGATOR_LLM_API_KEY)
  - 'stub'   : deterministic offline responder — used by the proof suite and
               the default for a fresh clone, so nothing breaks without a model

The app treats the model as a narrator, never an authority: everything it
writes is labeled 'perceived' until a human confirms or corrects it.
"""

from __future__ import annotations

import hashlib
import os

import httpx


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, cfg):
        self.backend = cfg.llm_backend
        self.url = cfg.llm_url.rstrip("/")
        self.model = cfg.llm_model
        self.timeout = cfg.llm_timeout

    def chat(self, system: str, user: str) -> str:
        if self.backend == "stub":
            return self._stub(system, user)
        if self.backend == "ollama":
            return self._ollama(system, user)
        if self.backend == "openai":
            return self._openai(system, user)
        raise LLMError(f"unknown llm backend: {self.backend}")

    def _stub(self, system: str, user: str) -> str:
        digest = hashlib.sha256((system + user).encode()).hexdigest()[:8]
        first = next((ln for ln in user.splitlines() if ln.strip()), "")[:120]
        return (f"[STUB:{digest}] Plain-language draft based on: {first}\n"
                "(No model is configured — this is a deterministic placeholder. "
                "Set [llm].backend in config.toml to 'ollama' or 'openai'.)")

    def _ollama(self, system: str, user: str) -> str:
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "stream": False,
            "think": False,
        }
        try:
            r = httpx.post(f"{self.url}/api/chat", json=body, timeout=self.timeout)
            r.raise_for_status()
            return r.json()["message"]["content"].strip()
        except (httpx.HTTPError, KeyError) as e:
            raise LLMError(f"ollama call failed ({self.url}): {e}") from e

    def _openai(self, system: str, user: str) -> str:
        headers = {}
        key = os.environ.get("NAVIGATOR_LLM_API_KEY")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
        }
        try:
            r = httpx.post(f"{self.url}/v1/chat/completions", json=body,
                           headers=headers, timeout=self.timeout)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except (httpx.HTTPError, KeyError, IndexError) as e:
            raise LLMError(f"openai-compatible call failed ({self.url}): {e}") from e
