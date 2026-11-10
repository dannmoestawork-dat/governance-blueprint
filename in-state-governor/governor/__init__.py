# SPDX-License-Identifier: Apache-2.0
"""In-State Governor — a deterministic governance-compliance checker.

Part of Governance Blueprint.

Design philosophy: STRUCTURE ENFORCES. This package is the mechanical core —
every check is a deterministic function with no model in the loop. A model may
advise, but only a deterministic check is a trust anchor; never rely on an LLM
to self-police.
"""

__version__ = "0.1.0"

from .rules import Finding, RULES, run_rule

__all__ = ["Finding", "RULES", "run_rule", "__version__"]
