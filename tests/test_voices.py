from __future__ import annotations

import responses

from saperly import VoiceListResult
from tests.conftest import BASE_URL, SAMPLE_VOICE


class TestVoices:
    def test_list_returns_result(self, mock_api, client):
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/api/v1/voices",
            json={"voices": [SAMPLE_VOICE]},
            status=200,
        )
        result = client.voices.list()

        assert isinstance(result, VoiceListResult)
        assert len(result.voices) == 1
        assert result.voices[0].slug == "aria"
        assert result.voices[0].name == "Aria"
        assert result.voices[0].gender == "female"
        assert result.voices[0].accent == "american"
        assert result.voices[0].description == "calm and conversational"
        assert result.voices[0].languages == ["multi"]
