from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class CispSettings:
    endpoint: str
    request_uri: str
    api_key: str
    timeout_seconds: float = 30.0
    verify_ssl: bool = True
    endpoint_proxy: str | None = None

    @property
    def query_url(self) -> str:
        return f"{self.endpoint.rstrip('/')}/{self.request_uri.lstrip('/')}"


def load_settings(api_key: str | None = None) -> CispSettings:
    load_dotenv()

    resolved_api_key = api_key or os.getenv("CISP_API_KEY")
    if not resolved_api_key:
        raise RuntimeError(
            "Missing CISP API key: HTTP clients must send "
            "'Authorization: Bearer <CISP_API_KEY>'; stdio clients must set CISP_API_KEY"
        )

    endpoint_proxy = os.getenv("CISP_ENDPOINT_PROXY")
    if endpoint_proxy is not None:
        endpoint_proxy = endpoint_proxy.strip() or None

    return CispSettings(
        endpoint=os.getenv("CISP_ENDPOINT", "https://cisp.zenitera.com"),
        request_uri=os.getenv("CISP_REQUEST_URI", "/ectcispserver/api/entcreditapi/query"),
        api_key=resolved_api_key,
        timeout_seconds=float(os.getenv("CISP_TIMEOUT_SECONDS", "60")),
        verify_ssl=_read_bool("CISP_VERIFY_SSL", True),
        endpoint_proxy=endpoint_proxy,
    )
