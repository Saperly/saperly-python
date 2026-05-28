"""Thin wrapper around crewai-tools' MCPServerAdapter for Saperly.

The Saperly hosted MCP server speaks the Streamable HTTP transport. CrewAI's
``MCPServerAdapter`` already handles that transport — the only thing this
helper adds is the right URL, the right transport name, and the
``Authorization`` bearer header. We keep the import lazy so users who don't
install crewai-tools don't pay the import cost (and get a clear error when
they do try to use the helper).

Usage::

    from saperly.crewai import SaperlyTools

    with SaperlyTools(api_key="sk_live_...") as tools:
        agent = Agent(role="phone caller", tools=tools)
        # ... build crew, run

If you'd rather manage the adapter lifecycle by hand, call
:func:`saperly_mcp_server_params` to get the dict you would pass directly to
``MCPServerAdapter(...)``.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ._client import DEFAULT_BASE_URL


def saperly_mcp_server_params(
    api_key: str,
    *,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Return the dict accepted by ``crewai_tools.MCPServerAdapter``.

    Streamable HTTP transport, the Saperly hosted MCP endpoint, and the
    bearer ``Authorization`` header. No CrewAI dependency at import time.
    """
    base = base_url or DEFAULT_BASE_URL
    return {
        "url": f"{base.rstrip('/')}/api/v1/mcp",
        "transport": "streamable-http",
        "headers": {"Authorization": f"Bearer {api_key}"},
    }


class SaperlyTools:
    """Context manager + factory that yields CrewAI tools for Saperly.

    Wraps ``crewai_tools.MCPServerAdapter`` so the user doesn't have to
    remember the URL, transport name, or header shape. Lazy-imports
    crewai-tools so install of ``saperly`` alone stays light.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: Optional[str] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self._params = saperly_mcp_server_params(api_key, base_url=base_url)
        self._adapter: Any = None

    def _build_adapter(self) -> Any:
        try:
            from crewai_tools import MCPServerAdapter  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ImportError(
                "saperly.crewai requires crewai-tools. Install with "
                "`pip install 'saperly[crewai]'` or `pip install crewai-tools`."
            ) from exc
        return MCPServerAdapter(self._params)

    def __enter__(self) -> Any:
        self._adapter = self._build_adapter()
        return self._adapter.__enter__()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> Optional[bool]:
        if self._adapter is None:
            return None
        try:
            return self._adapter.__exit__(exc_type, exc, tb)
        finally:
            self._adapter = None

    def start(self) -> Any:
        """Manual-lifecycle entry. Mirrors ``MCPServerAdapter.start``."""
        if self._adapter is not None:
            raise RuntimeError("SaperlyTools is already started")
        self._adapter = self._build_adapter()
        return self._adapter.start()

    def stop(self) -> None:
        """Manual-lifecycle exit. Mirrors ``MCPServerAdapter.stop``."""
        if self._adapter is None:
            return
        try:
            self._adapter.stop()
        finally:
            self._adapter = None

    @property
    def tools(self) -> Any:
        if self._adapter is None:
            raise RuntimeError("SaperlyTools is not started")
        return self._adapter.tools


__all__ = ["SaperlyTools", "saperly_mcp_server_params"]
