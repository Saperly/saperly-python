from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any

import pytest


def test_saperly_mcp_server_params_default_base_url() -> None:
    from saperly.crewai import saperly_mcp_server_params

    params = saperly_mcp_server_params("sk_live_test")
    assert params["url"].endswith("/api/v1/mcp")
    assert params["transport"] == "streamable-http"
    assert params["headers"] == {"Authorization": "Bearer sk_live_test"}


def test_saperly_mcp_server_params_custom_base_url_trims_trailing_slash() -> None:
    from saperly.crewai import saperly_mcp_server_params

    params = saperly_mcp_server_params(
        "sk_test_abc",
        base_url="http://localhost:3020/",
    )
    assert params["url"] == "http://localhost:3020/api/v1/mcp"


def test_saperly_tools_requires_api_key() -> None:
    from saperly.crewai import SaperlyTools

    with pytest.raises(ValueError):
        SaperlyTools(api_key="")


def test_saperly_tools_clear_error_when_crewai_tools_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Importing SaperlyTools without crewai-tools should fail with guidance."""
    from saperly.crewai import SaperlyTools

    # Force the lazy import path to fail even if crewai-tools is installed.
    original_import = __builtins__["__import__"] if isinstance(__builtins__, dict) else __import__

    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "crewai_tools":
            raise ImportError("simulated missing crewai_tools")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)
    tools = SaperlyTools(api_key="sk_live_test")
    with pytest.raises(ImportError) as info:
        tools.__enter__()
    assert "saperly[crewai]" in str(info.value)


def test_saperly_tools_context_manager_with_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    """When crewai_tools IS importable, SaperlyTools forwards to MCPServerAdapter."""
    stub_module = ModuleType("crewai_tools")

    captured: dict[str, Any] = {}

    class StubAdapter:
        def __init__(self, params: dict[str, Any]) -> None:
            captured["params"] = params
            self._entered = False

        def __enter__(self) -> str:
            self._entered = True
            return "stub-tools"

        def __exit__(self, *args: Any) -> None:
            self._entered = False

        def start(self) -> str:
            return "stub-tools"

        def stop(self) -> None:
            pass

        @property
        def tools(self) -> str:
            return "stub-tools"

    stub_module.MCPServerAdapter = StubAdapter  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "crewai_tools", stub_module)

    # Reload saperly.crewai so the lazy import resolves to the stub on next call.
    saperly_crewai = importlib.import_module("saperly.crewai")
    SaperlyTools = saperly_crewai.SaperlyTools

    with SaperlyTools(api_key="sk_live_test") as tools:
        assert tools == "stub-tools"

    assert captured["params"]["transport"] == "streamable-http"
    assert (
        captured["params"]["headers"]["Authorization"] == "Bearer sk_live_test"
    )
    assert captured["params"]["url"].endswith("/api/v1/mcp")
