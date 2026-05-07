from pathlib import Path
import tomllib


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_pypi_distribution_name_keeps_agentclaw_import_and_cli():
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "agentclaw-ai"
    package_include = pyproject["tool"]["setuptools"]["packages"]["find"]["include"]
    assert any(pattern == "agentclaw" or pattern.startswith("agentclaw*") for pattern in package_include)
    assert pyproject["project"]["scripts"]["agentclaw"] == "agentclaw.cli:main"


def test_default_pypi_install_includes_full_runtime_dependencies():
    pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = set(pyproject["project"]["dependencies"])
    expected = {
        "redis>=5.0.0",
        "markitdown[all]>=0.0.1",
        "pymilvus[milvus_lite]>=2.5.0",
        "APScheduler>=3.10.0,<4.0.0",
        "croniter>=2.0.0",
        "playwright>=1.52.0",
        "pywinauto>=0.6.8; platform_system == 'Windows'",
        "aiohttp>=3.8.0",
        "lark-oapi>=1.4.0",
        "dingtalk-stream>=0.9.0",
    }

    assert expected.issubset(dependencies)
