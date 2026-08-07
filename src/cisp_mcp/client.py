from __future__ import annotations

from typing import Any

import httpx

from .config import CispSettings
from .interfaces import CispInterface, INTERFACES, describe_product_status, describe_result_code


class CispApiClient:
    def __init__(self, settings: CispSettings) -> None:
        self._settings = settings

    async def post_json(
        self,
        payload: dict[str, Any],
        request_uri: str | None = None,
    ) -> dict[str, Any]:
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "X-API-Key": self._settings.api_key,
        }

        async with httpx.AsyncClient(
            timeout=self._settings.timeout_seconds,
            verify=self._settings.verify_ssl,
            proxy=self._settings.endpoint_proxy,
            trust_env=False,
        ) as client:
            response = await client.post(
                self._settings.query_url_for(request_uri),
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            return {
                "raw_text": response.text,
                "status_code": response.status_code,
            }

        if isinstance(data, dict):
            return data

        return {
            "data": data,
            "status_code": response.status_code,
        }

    async def query_product(
        self,
        prod_code: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:
        cleaned_params = clean_payload(params)
        payload: dict[str, Any] = {
            "prodCode": prod_code,
            **cleaned_params,
        }

        interface = INTERFACES.get(prod_code)
        raw_response = await self.post_json(
            payload,
            request_uri=interface.request_uri if interface else None,
        )
        if interface is None:
            return raw_response

        return normalize_interface_response(raw_response, interface)

    async def query_by_product_code(
        self,
        prod_code: str,
        ent_info: str,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"entInfo": ent_info}
        if extra_params:
            params.update(extra_params)
        return await self.query_product(prod_code=prod_code, params=params)

def clean_payload(params: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if not value:
                continue
        cleaned[key] = value
    return cleaned


def normalize_interface_response(
    raw_response: dict[str, Any],
    interface: CispInterface,
) -> dict[str, Any]:
    result_data = raw_response.get("resultData")
    if not isinstance(result_data, dict):
        result_data = {}

    product_data = result_data.get(interface.data_field)
    if not isinstance(product_data, dict):
        product_data = {}

    product_status = result_data.get(interface.status_field)
    if product_status is None:
        product_status = product_data.get(interface.status_field)
    result_code = raw_response.get("resultCode")

    normalized = {
        "product_code": interface.product_code,
        "interface_name": interface.name,
        "success": result_code == "00000",
        "has_result": str(product_status) == "4",
        "result_code": result_code,
        "result_code_desc": describe_result_code(result_code) or raw_response.get("resultDesc"),
        "result_desc": raw_response.get("resultDesc"),
        "product_status": product_status,
        "product_status_desc": describe_product_status(product_status),
        "order_no": raw_response.get("orderNo"),
        "packet_count": raw_response.get("packetCnt"),
        "is_compressed": raw_response.get("isCompressed"),
        "data": product_data,
        "raw_response": raw_response,
    }

    if interface.shortcut_field and interface.shortcut_field in product_data:
        normalized[interface.shortcut_field] = product_data[interface.shortcut_field]

    return normalized
