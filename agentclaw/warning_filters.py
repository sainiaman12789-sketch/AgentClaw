"""Targeted warning filters for noisy third-party startup warnings."""

from __future__ import annotations

import warnings


def install_warning_filters() -> None:
    """Install narrow warning filters that keep normal startup output readable."""

    warnings.filterwarnings(
        "ignore",
        message=r"The default value of `allowed_objects` will change in a future version\..*",
        category=Warning,
        module=r"langgraph\.checkpoint\.serde\.(encrypted|jsonplus)",
    )
