import warnings

from agentclaw.warning_filters import install_warning_filters


def test_allowed_objects_langgraph_startup_warning_is_filtered_without_hiding_other_warnings():
    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter("always")
        install_warning_filters()

        warnings.warn_explicit(
            "The default value of `allowed_objects` will change in a future version. "
            "Pass an explicit value (e.g., allowed_objects='messages' or 'core') to suppress this warning.",
            UserWarning,
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
