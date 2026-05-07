import warnings

from agentclaw.warning_filters import install_warning_filters


class _LangChainPendingDeprecationWarning(PendingDeprecationWarning):
    pass


def test_allowed_objects_langgraph_startup_warning_is_filtered_without_hiding_other_warnings():
    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter("always")
        with warnings.catch_warnings():
            pass
        install_warning_filters()

        warnings.warn_explicit(
            "The default value of `allowed_objects` will change in a future version. "
            "Pass an explicit value (e.g., allowed_objects='messages' or 'core') to suppress this warning.",
            PendingDeprecationWarning,
            filename="langgraph/checkpoint/serde/encrypted.py",
            lineno=5,
            module="langgraph.checkpoint.serde.encrypted",
        )
        warnings.warn_explicit(
            "different warning",
            UserWarning,
            filename="langgraph/checkpoint/serde/encrypted.py",
            lineno=6,
            module="langgraph.checkpoint.serde.encrypted",
        )

    assert len(records) == 1
    assert str(records[0].message) == "different warning"


def test_allowed_objects_warning_filter_uses_langchain_pending_warning_category(monkeypatch):
    import agentclaw.warning_filters as filters

    monkeypatch.setattr(
        filters,
        "_langchain_pending_deprecation_warning",
        lambda: _LangChainPendingDeprecationWarning,
    )

    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter("always")
        filters.install_warning_filters()

        warnings.warn(
            "The default value of `allowed_objects` will change in a future version. "
            "Pass an explicit value (e.g., allowed_objects='messages' or allowed_objects='core') to suppress this warning.",
            _LangChainPendingDeprecationWarning,
        )
        warnings.warn(
            "The default value of `allowed_objects` will change in a future version.",
            PendingDeprecationWarning,
        )
        warnings.warn(
            "Some other pending deprecation",
            PendingDeprecationWarning,
        )

    assert len(records) == 1
    assert records[0].category is PendingDeprecationWarning
    assert str(records[0].message) == "Some other pending deprecation"
