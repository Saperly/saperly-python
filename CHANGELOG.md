# saperly (Python) changelog

All notable changes to the Python SDK. Versions follow the platform release cadence.

## [0.4.0] (2026-05-28) CrewAI integration

### Added

- `saperly.crewai.SaperlyTools` context manager + `saperly_mcp_server_params(api_key)` helper. Wraps `crewai_tools.MCPServerAdapter` against the Saperly hosted MCP endpoint with the right URL, transport (streamable-http), and bearer `Authorization` header. Lazy imports `crewai_tools` so the dependency is opt-in.
- New `crewai` optional dependency: `pip install "saperly[crewai]"`.

## [0.3.0] (2026-05-13) agent-native key management

### Added

- `client.keys.*` resource: `create`, `list`, `get`, `update`, `rotate`, `delete`. Mint, rotate, and revoke child API keys from a service key (`sk_svc_…`).
- `client.audit.list()` unified audit feed: calls, SMS, compliance events, and billing scoped to the caller's key. Time-sorted DESC, max 500 events per call.
- New response field `created_by_service_key_id` on child API keys, so every call placed with a child key traces back to the service key that minted the credential.

### Fixed

- `child.plaintext_key` is the canonical attribute (a draft README example briefly showed `child.raw_key`. that attribute never existed on the dataclass).

### Notes

- Idempotency-Key header is required on `POST /v1/keys` and `POST /v1/keys/{id}/rotate`, and recommended on `POST /v1/calls` and `POST /v1/messages`. The client auto-generates a UUID v4 for the two key endpoints when one is not supplied; pass `idempotency_key` explicitly for cross-process retry safety.

## [0.2.0] (2026-04-28) Stripe payments foundation

### Changed

- Account balance reporting moved to cents-honest USD. `client.billing.balance()` returns USD cents.
- Webhook signature verification continues to use HMAC-SHA256 over `${timestamp}.${delivery_id}.${rawBody}` with a 5-minute clock-skew window. No public API changes for verification helpers.

## [0.1.0]

Initial release of the Saperly Python SDK.
