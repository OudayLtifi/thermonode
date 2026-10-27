from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from gateway.handler import Handler
from gateway.health import start_health_server


def test_health_metrics_and_unknown_routes(tmp_path):
    handler = Handler(tmp_path / "health.sqlite")
    handler.metrics["frames_received"] = 3
    server = start_health_server(handler, port=0)
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        with urlopen(base_url + "/health") as response:
            assert response.status == 200
            assert response.read() == b"ok"

        with urlopen(base_url + "/metrics") as response:
            assert response.status == 200
            assert response.read() == b"gateway_frames_received 3\n"

        with pytest.raises(HTTPError) as error:
            urlopen(base_url + "/unknown")
        assert error.value.code == 404
    finally:
        server.shutdown()
        server.server_close()
        handler.storage.close()
