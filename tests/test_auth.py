from __future__ import annotations

import os
import unittest
from typing import Any
from unittest.mock import patch

import httpx
from mcp.server.auth.provider import AccessToken

from cisp_mcp.client import CispApiClient
from cisp_mcp import server
from cisp_mcp.config import CispSettings, load_settings


class RecordingHttpClient:
    def __init__(self) -> None:
        self.headers: dict[str, str] | None = None

    async def __aenter__(self) -> RecordingHttpClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        return None

    async def post(
        self,
        url: str,
        *,
        json: dict[str, Any],
        headers: dict[str, str],
    ) -> httpx.Response:
        self.headers = headers
        return httpx.Response(
            200,
            json={"resultCode": "00000", "resultData": {}},
            request=httpx.Request("POST", url),
        )


class CispApiKeyTokenVerifierTests(unittest.IsolatedAsyncioTestCase):
    async def test_accepts_opaque_key_without_exposing_it_as_principal(self) -> None:
        api_key = "customer-key-123"

        access_token = await server.CispApiKeyTokenVerifier().verify_token(api_key)

        self.assertIsNotNone(access_token)
        assert access_token is not None
        self.assertEqual(access_token.token, api_key)
        self.assertEqual(access_token.scopes, ["cisp:query"])
        self.assertNotIn(api_key, access_token.client_id)
        self.assertEqual(access_token.client_id, access_token.subject)

    async def test_rejects_empty_or_malformed_keys(self) -> None:
        verifier = server.CispApiKeyTokenVerifier()

        for api_key in ("", " leading", "trailing ", "contains space", "line\nbreak"):
            with self.subTest(api_key=repr(api_key)):
                self.assertIsNone(await verifier.verify_token(api_key))


class RequestScopedClientTests(unittest.TestCase):
    def test_uses_bearer_token_for_current_request(self) -> None:
        access_token = AccessToken(
            token="customer-a-key",
            client_id="customer-a",
            scopes=["cisp:query"],
        )

        with patch("cisp_mcp.server.get_access_token", return_value=access_token):
            client = server.get_client()

        self.assertEqual(client._settings.api_key, "customer-a-key")

    def test_different_requests_receive_different_clients(self) -> None:
        customer_a = AccessToken(token="customer-a-key", client_id="a", scopes=["cisp:query"])
        customer_b = AccessToken(token="customer-b-key", client_id="b", scopes=["cisp:query"])

        with patch("cisp_mcp.server.get_access_token", return_value=customer_a):
            client_a = server.get_client()
        with patch("cisp_mcp.server.get_access_token", return_value=customer_b):
            client_b = server.get_client()

        self.assertEqual(client_a._settings.api_key, "customer-a-key")
        self.assertEqual(client_b._settings.api_key, "customer-b-key")

    def test_stdio_falls_back_to_environment_key(self) -> None:
        with (
            patch("cisp_mcp.server.get_access_token", return_value=None),
            patch.dict(os.environ, {"CISP_API_KEY": "stdio-key"}, clear=False),
        ):
            client = server.get_client()

        self.assertEqual(client._settings.api_key, "stdio-key")

    def test_missing_key_has_actionable_error(self) -> None:
        with (
            patch("cisp_mcp.config.load_dotenv"),
            patch.dict(os.environ, {}, clear=True),
        ):
            with self.assertRaisesRegex(RuntimeError, "Authorization: Bearer"):
                load_settings()

    def test_loads_optional_dedicated_proxy(self) -> None:
        with (
            patch("cisp_mcp.config.load_dotenv"),
            patch.dict(
                os.environ,
                {"CISP_ENDPOINT_PROXY": "  http://proxy.example.test:8080  "},
                clear=True,
            ),
        ):
            settings = load_settings(api_key="request-key")

        self.assertEqual(settings.endpoint_proxy, "http://proxy.example.test:8080")

    def test_blank_dedicated_proxy_means_direct_connection(self) -> None:
        with (
            patch("cisp_mcp.config.load_dotenv"),
            patch.dict(os.environ, {"CISP_ENDPOINT_PROXY": "  "}, clear=True),
        ):
            settings = load_settings(api_key="request-key")

        self.assertIsNone(settings.endpoint_proxy)


class CispApiClientAuthTests(unittest.IsolatedAsyncioTestCase):
    async def test_sends_request_key_as_cisp_x_api_key(self) -> None:
        http_client = RecordingHttpClient()
        client = CispApiClient(
            CispSettings(
                endpoint="https://cisp.example.test",
                request_uri="/query",
                api_key="customer-request-key",
            )
        )

        with patch(
            "cisp_mcp.client.httpx.AsyncClient",
            return_value=http_client,
        ) as async_client_class:
            await client.post_json({"prodCode": "P0010010"})

        self.assertIsNotNone(http_client.headers)
        assert http_client.headers is not None
        self.assertEqual(http_client.headers["X-API-Key"], "customer-request-key")
        async_client_class.assert_called_once_with(
            timeout=30.0,
            verify=True,
            proxy=None,
            trust_env=False,
        )

    async def test_uses_dedicated_cisp_proxy_when_configured(self) -> None:
        http_client = RecordingHttpClient()
        client = CispApiClient(
            CispSettings(
                endpoint="https://cisp.example.test",
                request_uri="/query",
                api_key="customer-request-key",
                endpoint_proxy="http://proxy.example.test:8080",
            )
        )

        with patch(
            "cisp_mcp.client.httpx.AsyncClient",
            return_value=http_client,
        ) as async_client_class:
            await client.post_json({"prodCode": "P0010010"})

        async_client_class.assert_called_once_with(
            timeout=30.0,
            verify=True,
            proxy="http://proxy.example.test:8080",
            trust_env=False,
        )


if __name__ == "__main__":
    unittest.main()
