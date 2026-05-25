from __future__ import annotations

import responses

from saperly import DeliveryListResult, WebhookDelivery, WebhookStats, WebhookTestResult
from tests.conftest import (
    BASE_URL,
    SAMPLE_DELIVERY,
    SAMPLE_INTERRUPTED_DELIVERY,
    SAMPLE_STATS_RAW,
)


class TestWebhooks:
    def test_deliveries(self, mock_api, client):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/api/v1/webhooks/deliveries",
            json={"deliveries": [SAMPLE_DELIVERY], "total": 1},
            status=200,
        )
        result = client.webhooks.deliveries()

        assert isinstance(result, DeliveryListResult)
        assert result.total == 1
        assert len(result.deliveries) == 1
        assert isinstance(result.deliveries[0], WebhookDelivery)
        assert result.deliveries[0].id == "del-1"
        assert result.deliveries[0].http_status == 200
        assert result.deliveries[0].duration_ms == 150

    def test_interrupted_delivery_shape(self, mock_api, client):
        """Phase Webhook Improvement Team 3: the `interrupted` event delivery
        shape round-trips through WebhookDelivery.from_dict with
        partial_response_text preserved in request_body."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/api/v1/webhooks/deliveries",
            json={"deliveries": [SAMPLE_INTERRUPTED_DELIVERY], "total": 1},
            status=200,
        )
        result = client.webhooks.deliveries(event_type="interrupted")

        assert result.total == 1
        delivery = result.deliveries[0]
        assert delivery.event_type == "interrupted"
        assert delivery.id == "del-2"
        # request_body carries the outbound interrupted event payload.
        # Verify partial_response_text round-trips through from_dict.
        assert isinstance(delivery.request_body, dict)
        assert delivery.request_body["event"] == "interrupted"
        assert "partial_response_text" in delivery.request_body

    def test_stats_transforms_camel(self, mock_api, client):
        """Verify camelCase keys from the API are transformed to snake_case on WebhookStats."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/api/v1/webhooks/stats",
            json=SAMPLE_STATS_RAW,
            status=200,
        )
        stats = client.webhooks.stats()

        assert isinstance(stats, WebhookStats)
        assert stats.success_rate == 0.95
        assert stats.by_event_type is not None
        assert len(stats.by_event_type) == 1
        assert stats.by_event_type[0]["event_type"] == "call_started"
        assert stats.by_hour is not None
        assert len(stats.by_hour) == 1
        assert stats.by_hour[0]["hour"] == "2026-01-01T00:00:00Z"

    def test_test_webhook(self, mock_api, client):
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/api/v1/webhooks/test",
            json={
                "delivery": {
                    "id": "del-test",
                    "status": "success",
                    "http_status": 200,
                    "duration_ms": 50,
                    "response_body": "ok",
                },
            },
            status=200,
        )
        result = client.webhooks.test(line_id="line-1")

        assert isinstance(result, WebhookTestResult)
        assert result.delivery is not None
        assert result.delivery["id"] == "del-test"
        assert result.delivery["status"] == "success"
        assert result.delivery["http_status"] == 200
        assert result.delivery["duration_ms"] == 50
        assert result.delivery["response_body"] == "ok"
