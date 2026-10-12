import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def _free_port():
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _wait(url, timeout=5):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with urlopen(url, timeout=.5) as response:
                return response.status
        except Exception:
            time.sleep(.05)
    raise AssertionError("server did not become ready: " + url)


def test_web_server_proxies_api_to_local_backend():
    api_port = _free_port()
    web_port = _free_port()
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{ROOT / 'src'}:{ROOT}"
    env["NEXTLAW_API_PORT"] = str(api_port)
    api = subprocess.Popen([sys.executable, "scripts/api_fallback.py"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    web_env = env.copy()
    web_env["PORT"] = str(web_port)
    web_env["NEXTLAW_API_ORIGIN"] = f"http://127.0.0.1:{api_port}"
    web = subprocess.Popen(["node", "server.mjs"], cwd=ROOT / "apps" / "web", env=web_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert _wait(f"http://127.0.0.1:{api_port}/status/live") == 200
        assert _wait(f"http://127.0.0.1:{web_port}/") == 200
        request = Request(
            f"http://127.0.0.1:{web_port}/api/live",
            data=json.dumps({"mode": "search", "user_goal": "protect my rights"}).encode(),
            headers={"content-type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=2) as response:
            payload = json.loads(response.read())
        assert response.status == 200
        assert "say_now" in payload
    finally:
        web.terminate(); api.terminate()
        web.wait(timeout=3); api.wait(timeout=3)
