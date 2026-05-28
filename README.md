# saperly

Python client for the Saperly API. The phone carrier for AI agents.

One API call gives your agent a real phone number with TCPA compliance, consent capture, and an audit trail built in. Python 3.9+. Sync via `requests`; optional async via `httpx`.

## Install

```bash
pip install saperly
```

For the async client:

```bash
pip install "saperly[async]"
```

For the CrewAI tool wrapper:

```bash
pip install "saperly[crewai]"
```

## Use with CrewAI

Saperly ships a Streamable HTTP MCP endpoint at `https://saperly.com/api/v1/mcp`. The CrewAI helper wraps `crewai_tools.MCPServerAdapter` with the right URL, transport, and bearer header.

```python
import os
from crewai import Agent
from saperly.crewai import SaperlyTools

with SaperlyTools(api_key=os.environ["SAPERLY_API_KEY"]) as tools:
    agent = Agent(
        role="phone caller",
        goal="Call leads, qualify them, log results.",
        tools=tools,
    )
    # ... build crew and run
```

Prefer to manage the lifecycle by hand? Call `SaperlyTools.start()` / `SaperlyTools.stop()`, or use `saperly_mcp_server_params(api_key)` to get the dict you'd pass to `MCPServerAdapter(...)` directly.

## Quickstart

Provision a hosted line and print its phone number.

```python
import os
from saperly import SaperlyClient

saperly = SaperlyClient(api_key=os.environ["SAPERLY_API_KEY"])

line = saperly.lines.create(
    name="my agent",
    mode="hosted",
    system_prompt="You are a helpful assistant.",
)

print(line.phone_number)
```

Get an API key at [saperly.com/settings/keys](https://saperly.com/settings/keys). Signup is portal-only (magic link, Google, or GitHub).

## Auth

Saperly uses a two-tier credential model. Both authenticate via `Authorization: Bearer <key>`.

| Credential | Use case |
| --- | --- |
| API key (`sk_live_…`, `sk_test_…`) | Place calls, send SMS, manage lines, read usage and audit. |
| Service key (`sk_svc_live_…`, `sk_svc_test_…`) | Mint, rotate, and revoke child API keys via `POST /v1/keys`. Credential management only. |

Child API keys minted by a service key carry their own scope: `full`, `call_only`, `sms_only`, or `read_only`, optionally bound to a single `line_id` with a `monthly_cap_cents` ceiling. Full reference at [docs.saperly.com/service-keys](https://docs.saperly.com/service-keys).

## Resources

- Docs: https://docs.saperly.com
- Quickstart: https://docs.saperly.com/quickstart
- Agent onboarding: https://docs.saperly.com/agent-onboarding
- Service keys: https://docs.saperly.com/service-keys
- Patterns and pitfalls: [./AGENTS.md](./AGENTS.md)
- API reference: https://docs.saperly.com/api-reference
- Issues: https://github.com/Saperly/saperly-python/issues
- Discord: invite link in our docs

## License

MIT. See [LICENSE](./LICENSE).

## Contact

hello@saperly.com or open an issue.
