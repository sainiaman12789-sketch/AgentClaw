from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from agentclaw.channels.wecom import WeComChannel


def _node_process():
    return SimpleNamespace(stdout=None, stderr=None, returncode=0)


@pytest.mark.asyncio
async def test_wecom_bot_start_installs_missing_worker_dependencies_before_launch(tmp_path):
    worker_dir = tmp_path / "wecom_worker"
    worker_dir.mkdir()
    worker_script = worker_dir / "worker.mjs"
    worker_script.write_text("import '@wecom/aibot-node-sdk';\n", encoding="utf-8")

    channel = WeComChannel(bot_id="bot-id", secret="secret")

    npm_process = SimpleNamespace(returncode=0)

    async def communicate():
        sdk_dir = worker_dir / "node_modules" / "@wecom" / "aibot-node-sdk"
        sdk_dir.mkdir(parents=True)
        (sdk_dir / "package.json").write_text("{}", encoding="utf-8")
        return b"installed", b""

    npm_process.communicate = communicate

    async def create_process(*args, **kwargs):
        if args[1] == "install":
            return npm_process
        return _node_process()

    with (
        patch("agentclaw.channels.wecom.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"),
        patch("agentclaw.channels.wecom.Path.resolve", return_value=tmp_path / "wecom.py"),
        patch("agentclaw.channels.wecom.asyncio.create_subprocess_exec", AsyncMock(side_effect=create_process)) as popen,
        patch.object(channel, "_wait_for_worker_ready", AsyncMock()),
    ):
        await channel._start_bot_worker()

    npm_call = popen.await_args_list[0].args
    node_call = popen.await_args_list[1].args
    assert npm_call[:2] == ("/usr/bin/npm", "install")
    assert "--omit=dev" in npm_call
    assert node_call == ("/usr/bin/node", str(worker_script))


@pytest.mark.asyncio
async def test_wecom_bot_start_skips_worker_dependency_install_when_present(tmp_path):
    worker_dir = tmp_path / "wecom_worker"
    sdk_dir = worker_dir / "node_modules" / "@wecom" / "aibot-node-sdk"
    sdk_dir.mkdir(parents=True)
    (sdk_dir / "package.json").write_text("{}", encoding="utf-8")
    worker_script = worker_dir / "worker.mjs"
    worker_script.write_text("import '@wecom/aibot-node-sdk';\n", encoding="utf-8")

    channel = WeComChannel(bot_id="bot-id", secret="secret")

    with (
        patch("agentclaw.channels.wecom.shutil.which", side_effect=lambda name: f"/usr/bin/{name}"),
        patch("agentclaw.channels.wecom.Path.resolve", return_value=tmp_path / "wecom.py"),
        patch("agentclaw.channels.wecom.asyncio.create_subprocess_exec", AsyncMock(return_value=_node_process())) as popen,
        patch.object(channel, "_wait_for_worker_ready", AsyncMock()),
    ):
        await channel._start_bot_worker()

    assert len(popen.await_args_list) == 1
    assert popen.await_args.args == ("/usr/bin/node", str(worker_script))
