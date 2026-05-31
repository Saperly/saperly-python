from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _pick(data: Dict[str, Any], cls: type) -> Dict[str, Any]:
    """Extract only the keys that match dataclass fields, returning None for missing."""
    fields = {f.name for f in dataclasses.fields(cls)}
    return {k: data.get(k) for k in fields}


# ---------------------------------------------------------------------------
# Core resources
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Line:
    id: Optional[str] = None
    phone_number: Optional[str] = None
    display_name: Optional[str] = None
    name: Optional[str] = None
    mode: Optional[str] = None
    audio_handler_url: Optional[str] = None
    webhook_url: Optional[str] = None
    status_callback_url: Optional[str] = None
    status: Optional[str] = None
    environment: Optional[str] = None
    created_at: Optional[str] = None
    system_prompt: Optional[str] = None
    begin_message: Optional[str] = None
    voice: Optional[str] = None
    context_limit: Optional[int] = None
    recording_enabled: Optional[bool] = None
    compliance_enabled: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Line:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Call:
    id: Optional[str] = None
    line_id: Optional[str] = None
    direction: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    status: Optional[str] = None
    duration_sec: Optional[int] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    created_at: Optional[str] = None
    recording_url: Optional[str] = None
    transcript: Optional[List[Dict[str, Any]]] = None
    system_prompt: Optional[str] = None
    begin_message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Call:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class ConsentRecord:
    id: Optional[str] = None
    phone_number: Optional[str] = None
    line_id: Optional[str] = None
    consent_type: Optional[str] = None
    status: Optional[str] = None
    granted_at: Optional[str] = None
    revoked_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConsentRecord:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class ConsentCheckResult:
    status: Optional[str] = None
    consent: Optional[ConsentRecord] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ConsentCheckResult:
        consent_data = data.get("consent")
        consent = ConsentRecord.from_dict(consent_data) if isinstance(consent_data, dict) else None
        return cls(status=data.get("status"), consent=consent)


@dataclass(frozen=True)
class ComplianceEvent:
    id: Optional[str] = None
    line_id: Optional[str] = None
    call_id: Optional[str] = None
    phone_number: Optional[str] = None
    event_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ComplianceEvent:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Disclosure:
    id: Optional[str] = None
    message: Optional[str] = None
    audio_url: Optional[str] = None
    language: Optional[str] = None
    jurisdiction: Optional[str] = None
    is_default: Optional[bool] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Disclosure:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Balance:
    """
    Account balance.

    v0.5.3 cents-honest pivot: the ``credits`` field carries US cents (e.g.
    ``500`` = $5.00). The historical name is preserved for backward-compat
    with v0.5.1.x clients; rename to ``cents`` is deferred to v0.6.x.

    The ``cents`` field is added here as the v1.0-stable name. On servers
    >= v0.5.3 it is populated and equals ``credits``; on older servers it
    is ``None`` and callers should fall back to ``credits``.

    The ``currency`` field returns ``"USD"`` on servers >= v0.5.3 and the
    legacy ``"credits"`` literal on older servers.
    """

    credits: Optional[int] = None
    cents: Optional[int] = None
    currency: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Balance:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Transaction:
    """
    Billing transaction record.

    v0.5.3 cents-honest pivot: ``amount_credits`` and ``balance_after_credits``
    carry US cents, not credit units. The historical names are preserved for
    backward-compat with v0.5.1.x clients; rename to ``*_cents`` is deferred
    to v0.6.x. To display as dollars: ``f"${amount_credits / 100:.2f}"``.
    """

    id: Optional[str] = None
    type: Optional[str] = None
    amount_credits: Optional[int] = None
    balance_after_credits: Optional[int] = None
    description: Optional[str] = None
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transaction:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class TransactionListResult:
    transactions: Optional[List[Transaction]] = None
    has_more: Optional[bool] = None
    next_cursor: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TransactionListResult:
        raw = data.get("transactions", [])
        transactions = [Transaction.from_dict(t) for t in raw] if isinstance(raw, list) else []
        return cls(
            transactions=transactions,
            has_more=data.get("has_more"),
            next_cursor=data.get("next_cursor"),
        )


@dataclass(frozen=True)
class AddFundsResult:
    checkout_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AddFundsResult:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class SmsMessage:
    id: Optional[str] = None
    from_number: Optional[str] = None
    to_number: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SmsMessage:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Message:
    id: Optional[str] = None
    line_id: Optional[str] = None
    to: Optional[str] = None
    text: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Conversation:
    line_id: Optional[str] = None
    phone_number: Optional[str] = None
    line_phone_number: Optional[str] = None
    message_count: Optional[int] = None
    last_message_at: Optional[str] = None
    last_message_text: Optional[str] = None
    last_message_direction: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Conversation":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class ConversationListResult:
    conversations: Optional[List[Conversation]] = None
    has_more: Optional[bool] = None
    next_cursor: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationListResult":
        convos = [Conversation.from_dict(c) for c in data.get("conversations", [])]
        return cls(
            conversations=convos,
            has_more=data.get("has_more"),
            next_cursor=data.get("next_cursor"),
        )


@dataclass(frozen=True)
class ConversationMessage:
    direction: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationMessage":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class ConversationMessagesResult:
    messages: Optional[List[ConversationMessage]] = None
    has_more: Optional[bool] = None
    next_cursor: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationMessagesResult":
        msgs = [ConversationMessage.from_dict(m) for m in data.get("messages", [])]
        return cls(
            messages=msgs,
            has_more=data.get("has_more"),
            next_cursor=data.get("next_cursor"),
        )


@dataclass(frozen=True)
class DailyUsage:
    date: Optional[str] = None
    calls: Optional[int] = None
    minutes: Optional[int] = None
    sms_inbound: Optional[int] = None
    sms_outbound: Optional[int] = None
    cost_credits: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyUsage":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class DailyUsageResult:
    daily: Optional[List[DailyUsage]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyUsageResult":
        items = [DailyUsage.from_dict(d) for d in data.get("daily", [])]
        return cls(daily=items)


@dataclass(frozen=True)
class MonthlyUsage:
    month: Optional[str] = None
    calls: Optional[int] = None
    minutes: Optional[int] = None
    sms_inbound: Optional[int] = None
    sms_outbound: Optional[int] = None
    cost_credits: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MonthlyUsage":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class MonthlyUsageResult:
    monthly: Optional[List[MonthlyUsage]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MonthlyUsageResult":
        items = [MonthlyUsage.from_dict(m) for m in data.get("monthly", [])]
        return cls(monthly=items)


@dataclass(frozen=True)
class Settings:
    default_webhook_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Settings":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class Voice:
    # Saperly voice slug — set as a line's `voice`. Never a vendor voice id.
    slug: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    accent: Optional[str] = None
    description: Optional[str] = None
    languages: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Voice":
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class VoiceListResult:
    voices: Optional[List[Voice]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoiceListResult":
        items = [Voice.from_dict(v) for v in data.get("voices", [])]
        return cls(voices=items)


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WebhookDelivery:
    id: Optional[str] = None
    line_id: Optional[str] = None
    call_id: Optional[str] = None
    event_type: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    http_status: Optional[int] = None
    error_message: Optional[str] = None
    attempt_count: Optional[int] = None
    request_body: Optional[Any] = None
    response_body: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookDelivery:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class WebhookStats:
    total: Optional[int] = None
    success: Optional[int] = None
    failed: Optional[int] = None
    success_rate: Optional[float] = None
    by_event_type: Optional[List[Dict[str, Any]]] = None
    by_hour: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookStats:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class WebhookTestResult:
    delivery: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> WebhookTestResult:
        return cls(**_pick(data, cls))


# ---------------------------------------------------------------------------
# List / paginated results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CallListResult:
    calls: Optional[List[Call]] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CallListResult:
        raw_calls = data.get("calls", [])
        calls = [Call.from_dict(c) for c in raw_calls] if isinstance(raw_calls, list) else []
        return cls(calls=calls, total=data.get("total"))


@dataclass(frozen=True)
class AuditResult:
    events: Optional[List[ComplianceEvent]] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AuditResult:
        raw_events = data.get("events", [])
        events = (
            [ComplianceEvent.from_dict(e) for e in raw_events]
            if isinstance(raw_events, list)
            else []
        )
        return cls(events=events, total=data.get("total"))


@dataclass(frozen=True)
class UnifiedAuditEvent:
    """Single event from /v1/audit unified feed.

    `type` discriminates the source table; `data` is a heterogeneous payload
    whose snake_case shape depends on `type`. v1 keeps the data field as a
    plain dict — narrow via the type field at the call site.
    """

    type: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UnifiedAuditEvent:
        return cls(
            type=data.get("type"),
            id=data.get("id"),
            created_at=data.get("created_at"),
            data=data.get("data"),
        )


@dataclass(frozen=True)
class UnifiedAuditResult:
    """Result of /v1/audit unified-feed list call."""

    events: Optional[List[UnifiedAuditEvent]] = None
    limit: Optional[int] = None
    api_key_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> UnifiedAuditResult:
        raw_events = data.get("events", [])
        events = (
            [UnifiedAuditEvent.from_dict(e) for e in raw_events]
            if isinstance(raw_events, list)
            else []
        )
        return cls(
            events=events,
            limit=data.get("limit"),
            api_key_id=data.get("api_key_id"),
        )


@dataclass(frozen=True)
class DeliveryListResult:
    deliveries: Optional[List[WebhookDelivery]] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DeliveryListResult:
        raw = data.get("deliveries", [])
        deliveries = (
            [WebhookDelivery.from_dict(d) for d in raw] if isinstance(raw, list) else []
        )
        return cls(deliveries=deliveries, total=data.get("total"))


# ---------------------------------------------------------------------------
# API Keys (child keys minted by a service key)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ApiKey:
    id: Optional[str] = None
    key_prefix: Optional[str] = None
    environment: Optional[str] = None
    name: Optional[str] = None
    agent_label: Optional[str] = None
    line_id: Optional[str] = None
    permissions: Optional[str] = None
    monthly_cap_cents: Optional[int] = None
    monthly_spend_cents: Optional[int] = None
    created_at: Optional[str] = None
    revoked_at: Optional[str] = None
    last_used_at: Optional[str] = None
    rotated_from: Optional[str] = None
    created_by_service_key_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ApiKey:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class CreateApiKeyResponse:
    """Response from .keys.create() and .keys.rotate(). plaintext_key returned ONCE."""

    id: Optional[str] = None
    plaintext_key: Optional[str] = None
    key_prefix: Optional[str] = None
    environment: Optional[str] = None
    name: Optional[str] = None
    agent_label: Optional[str] = None
    line_id: Optional[str] = None
    permissions: Optional[str] = None
    monthly_cap_cents: Optional[int] = None
    monthly_spend_cents: Optional[int] = None
    created_at: Optional[str] = None
    revoked_at: Optional[str] = None
    last_used_at: Optional[str] = None
    rotated_from: Optional[str] = None
    created_by_service_key_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CreateApiKeyResponse:
        return cls(**_pick(data, cls))


@dataclass(frozen=True)
class ApiKeyListResult:
    keys: Optional[List[ApiKey]] = None
    total: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ApiKeyListResult:
        raw = data.get("keys", [])
        items = [ApiKey.from_dict(k) for k in raw] if isinstance(raw, list) else []
        return cls(keys=items, total=data.get("total"))
