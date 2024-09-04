import pytest

from dl_api_commons.client.base import Req


@pytest.mark.asyncio
async def test_yandex_token(oauth_app_client):
    resp = await oauth_app_client.make_request(
        Req(
            method="post",
            url="/oauth/token/yandex",
            data_json={
                "conn_type": "metrica",
                "code": "1234567",
            },
        )
    )
    assert resp.status == 200
    assert "error" in resp.json
    assert resp.json["error"] == "invalid_client"
