"""Targeted warning filters for noisy third-party startup warnings."""

from __future__ import annotations

import warnings


def _langchain_pending_deprecation_warning() -> type[Warning]:
    try:
        from langchain_core._api.deprecation import LangChainPendingDeprecationWarning

        return LangChainPendingDeprecationWarning
    except Exception:
        return PendingDeprecationWarning


def install_warning_filters() -> None:
    """Install narrow warning filters that keep normal startup output readable."""

    message = r"The default value of `allowed_objects` will change in a future version\..*"
    for category in {_langchain_pending_deprecation_warning(), PendingDeprecationWarning}:
        warnings.filterwarnings(
            "ignore",
            message=message,
            category=category,
        )
