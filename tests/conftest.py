from __future__ import annotations

import pytest
import responses

from saperly import SaperlyClient

BASE_URL = "http://test"


@pytest.fixture
def mock_api():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def client():
    return SaperlyClient(api_key="sk_test_123", base_url=BASE_URL)


# ---------------------------------------------------------------------------
# Sample data constants (snake_case — matching post-transform API responses)
# ---------------------------------------------------------------------------

SAMPLE_LINE = {
    "id": "line-1",
    "phone_number": "+14155550123",
    "display_name": None,
    "name": "support",
    "mode": "text",
    "audio_handler_url": None,
    "webhook_url": "https://example.com/hook",
    "status_callback_url": None,
    "status": "active",
    "environment": "live",
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_CALL = {
    "id": "call-1",
    "line_id": "line-1",
    "direction": "outbound",
    "from_number": "+14155550123",
    "to_number": "+14155559999",
    "status": "initiated",
    "duration_sec": None,
    "started_at": None,
    "ended_at": None,
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_CONSENT = {
    "id": "consent-1",
    "phone_number": "+14155559999",
    "line_id": "line-1",
    "consent_type": "explicit_outbound",
    "status": "active",
    "granted_at": "2026-01-01T00:00:00Z",
    "revoked_at": None,
}

SAMPLE_EVENT = {
    "id": "event-1",
    "line_id": "line-1",
    "call_id": "call-1",
    "phone_number": "+14155559999",
    "event_type": "call_started",
    "metadata": {"source": "outbound"},
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_DISCLOSURE = {
    "id": "disc-1",
    "message": "This call uses AI.",
    "audio_url": None,
    "language": "en",
    "jurisdiction": "us",
    "is_default": True,
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_DELIVERY = {
    "id": "del-1",
    "line_id": "line-1",
    "call_id": "call-1",
    "event_type": "call_started",
    "url": "https://example.com/hook",
    "status": "success",
    "http_status": 200,
    "error_message": None,
    "attempt_count": 1,
    "request_body": {},
    "response_body": "ok",
    "duration_ms": 150,
    "created_at": "2026-01-01T00:00:00Z",
}

# Phase Webhook Improvement Team 3: barge-in `interrupted` delivery shape.
# partial_response_text carries the prefix Twilio confirmed playing — may be
# empty when caller barges in before any audio is acknowledged.
SAMPLE_INTERRUPTED_DELIVERY = {
    "id": "del-2",
    "line_id": "line-1",
    "call_id": "call-1",
    "event_type": "interrupted",
    "url": "https://example.com/hook",
    "status": "success",
    "http_status": 200,
    "error_message": None,
    "attempt_count": 1,
    "request_body": {
        "event": "interrupted",
        "call_id": "call-1",
        "timestamp": 1779441656686,
        "partial_response_text": "Of course, I would be delighted to tell you everything.",
    },
    "response_body": "ok",
    "duration_ms": 42,
    "created_at": "2026-05-23T00:00:00Z",
}

SAMPLE_MESSAGE = {
    "id": "msg_1",
    "line_id": "line_1",
    "to": "+15551234567",
    "text": "Hello",
    "status": "sent",
    "created_at": "2026-01-01T00:00:00Z",
}

SAMPLE_CONVERSATION = {
    "line_id": "line_1",
    "phone_number": "+15551234567",
    "line_phone_number": "+15559876543",
    "message_count": 5,
    "last_message_at": "2026-01-01T00:00:00Z",
    "last_message_text": "Hi there",
    "last_message_direction": "inbound",
}

SAMPLE_DAILY_USAGE = {
    "date": "2026-01-01",
    "calls": 10,
    "minutes": 45,
    "sms_inbound": 3,
    "sms_outbound": 2,
    "cost_credits": 495,
}

SAMPLE_MONTHLY_USAGE = {
    "month": "2026-01",
    "calls": 100,
    "minutes": 450,
    "sms_inbound": 30,
    "sms_outbound": 20,
    "cost_credits": 4950,
}

SAMPLE_SETTINGS = {
    "default_webhook_url": "https://example.com/webhook",
}

SAMPLE_VOICE = {
    "id": "voice_1",
    "name": "Alloy",
    "gender": "female",
    "accent": "american",
    "style": "conversational",
}

# Stats come from API in camelCase (webhook stats endpoint doesn't use format layer)
SAMPLE_STATS_RAW = {
    "total": 100,
    "success": 95,
    "failed": 5,
    "successRate": 0.95,
    "byEventType": [
        {"eventType": "call_started", "total": 50, "success": 48, "failed": 2},
    ],
    "byHour": [
        {"hour": "2026-01-01T00:00:00Z", "total": 10, "success": 9, "failed": 1},
    ],
}
