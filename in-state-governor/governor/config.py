# SPDX-License-Identifier: Apache-2.0
"""TOML config loading for In-State Governor.

The config declares which rules are enabled and their parameters. Format::

    [[rule]]
    id = "required_header"
    glob = "**/*.md"
    pattern = "^## Classification:"
    severity = "error"

Each ``[[rule]]`` table needs an ``id`` that matches a key in
:data:`governor.rules.RULES`; all other keys are passed through to the rule as
its ``params`` dict. A rule may appear more than once (e.g. different globs).
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass

from .rules import RULES


@dataclass
class RuleConfig:
    rule_id: str
    params: dict


@dataclass
class Config:
    rules: list[RuleConfig]

    @property
    def enabled_ids(self) -> list[str]:
        return [r.rule_id for r in self.rules]


def load_config(path: str) -> Config:
    """Load and validate a TOML config file."""
    with open(path, "rb") as fh:
        raw = tomllib.load(fh)
    return _parse(raw, source=path)


def load_config_str(text: str, source: str = "<string>") -> Config:
    """Load a config from a TOML string (used in tests)."""
    return _parse(tomllib.loads(text), source=source)


def _parse(raw: dict, source: str) -> Config:
    rule_tables = raw.get("rule")
    if rule_tables is None:
        raise ValueError(f"{source}: config has no [[rule]] tables.")
    if not isinstance(rule_tables, list):
        raise ValueError(f"{source}: 'rule' must be an array of tables ([[rule]]).")

    rules: list[RuleConfig] = []
    for i, table in enumerate(rule_tables):
        if not isinstance(table, dict):
            raise ValueError(f"{source}: [[rule]] #{i} is not a table.")
        if "id" not in table:
            raise ValueError(f"{source}: [[rule]] #{i} is missing 'id'.")
        rule_id = table["id"]
        if rule_id not in RULES:
            raise ValueError(
                f"{source}: [[rule]] #{i} has unknown id '{rule_id}'. "
                f"Known rules: {sorted(RULES)}"
            )
        params = {k: v for k, v in table.items() if k != "id"}
        rules.append(RuleConfig(rule_id=rule_id, params=params))

    if not rules:
        raise ValueError(f"{source}: no rules enabled.")
    return Config(rules=rules)
