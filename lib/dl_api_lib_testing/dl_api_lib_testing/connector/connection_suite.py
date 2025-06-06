import json
from typing import Optional
import uuid

import pytest

from dl_api_client.dsmaker.api.http_sync_base import SyncHttpClientBase
from dl_api_lib.app_settings import ControlApiAppSettings
from dl_api_lib.schemas.connection import GenericConnectionSchema
from dl_api_lib_testing.connection_base import ConnectionTestBase
from dl_constants.api_constants import DLHeadersCommon
from dl_core.connectors.base.export_import import is_export_import_allowed
from dl_core.us_connection_base import ConnectionBase
from dl_core.us_manager.us_manager_sync import SyncUSManager
from dl_testing.regulated_test import RegulatedTestCase


class DefaultConnectorConnectionTestSuite(ConnectionTestBase, RegulatedTestCase):
    def test_create_connection(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
    ) -> None:
        assert saved_connection_id
        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/{saved_connection_id}",
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json

    def test_export_connection(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
        sync_us_manager: SyncUSManager,
        control_api_app_settings: ControlApiAppSettings,
    ) -> None:
        conn = sync_us_manager.get_by_id(saved_connection_id, expected_type=ConnectionBase)
        assert isinstance(conn, ConnectionBase)

        us_master_token = control_api_app_settings.US_MASTER_TOKEN
        assert us_master_token

        if bi_headers is None:
            bi_headers = dict()

        bi_headers[DLHeadersCommon.US_MASTER_TOKEN.value] = us_master_token

        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/export/{saved_connection_id}",
            headers=bi_headers,
        )

        if not is_export_import_allowed(self.conn_type):
            assert resp.status_code == 200, resp.json
            assert "notifications" in resp.json, resp.json
            assert resp.json["notifications"][0]["code"] == "ERR.DS_API.UNSUPPORTED", resp.json
            return

        assert resp.status_code == 200, resp.json
        conn_edit_schema_cls = GenericConnectionSchema().get_edit_schema_cls(conn)
        if hasattr(conn_edit_schema_cls(), "password"):
            # TODO check all secret fields according to conn.data.get_secret_keys(), not just "password"
            password = resp.json["connection"]["password"]
            assert password == "******"

    def test_import_connection(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
        sync_us_manager: SyncUSManager,
        control_api_app_settings: ControlApiAppSettings,
    ) -> None:
        conn = sync_us_manager.get_by_id(saved_connection_id, expected_type=ConnectionBase)
        assert isinstance(conn, ConnectionBase)
        if not is_export_import_allowed(self.conn_type):
            return

        us_master_token = control_api_app_settings.US_MASTER_TOKEN
        assert us_master_token

        if bi_headers is None:
            bi_headers = dict()

        bi_headers[DLHeadersCommon.US_MASTER_TOKEN.value] = us_master_token

        # test invalid request
        import_request = json.dumps({})

        import_response = control_api_sync_client.post(
            url="/api/v1/connections/import",
            headers=bi_headers,
            data=import_request,
            content_type="application/json",
        )
        assert import_response.status_code == 400

        # test common import
        export_resp = control_api_sync_client.get(
            url=f"/api/v1/connections/export/{saved_connection_id}",
            headers=bi_headers,
        )

        export_resp.json["connection"][
            "name"
        ] = f"{self.conn_type.name} conn {uuid.uuid4()}"  # in case of response with workbook, 'name'-field is in export response by default

        import_request = json.dumps(
            {
                "data": {
                    # "workbook_id" : "1234567890000", # can't test with workbook in case of ERR.DS_API.US.OBJ_NOT_FOUND
                    "connection": export_resp.json["connection"]
                }
            }
        )

        import_response = control_api_sync_client.post(
            url="/api/v1/connections/import",
            headers=bi_headers,
            data=import_request,
            content_type="application/json",
        )
        assert import_response.status_code == 200, import_response.json
        assert import_response.json["id"]
        assert import_response.json["id"] != saved_connection_id
        conn_edit_schema_cls = GenericConnectionSchema().get_edit_schema_cls(conn)
        if hasattr(conn_edit_schema_cls(), "password"):
            # TODO check all secret fields according to conn.data.get_secret_keys(), not just "password"
            assert import_response.json["notifications"]
            assert any(
                "CHECK_CREDENTIALS" in notification["code"] for notification in import_response.json["notifications"]
            )

        export_resp = control_api_sync_client.delete(
            url=f"/api/v1/connections/{import_response.json['id']}",
            headers=bi_headers,
        )

    def test_test_connection(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
    ) -> None:
        resp = control_api_sync_client.post(
            f"/api/v1/connections/test_connection/{saved_connection_id}",
            content_type="application/json",
            data=json.dumps({}),
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json

    def test_cache_ttl_sec_override(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
    ) -> None:
        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/{saved_connection_id}",
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json
        assert resp.json["cache_ttl_sec"] is None, resp.json

        cache_ttl_override = 100500
        resp = control_api_sync_client.put(
            url=f"/api/v1/connections/{saved_connection_id}",
            content_type="application/json",
            data=json.dumps({"cache_ttl_sec": cache_ttl_override}),
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json

        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/{saved_connection_id}",
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json
        assert resp.json["cache_ttl_sec"] == cache_ttl_override, resp.json

    def test_connection_options(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
    ) -> None:
        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/{saved_connection_id}",
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json
        assert isinstance(resp.json["options"]["allow_dashsql_usage"], bool)
        assert isinstance(resp.json["options"]["allow_dataset_usage"], bool)
        assert isinstance(resp.json["options"]["allow_typed_query_usage"], bool)
        assert len(resp.json["options"]["query_types"]) > 0
        assert any([qt["query_type"] == "generic_query" for qt in resp.json["options"]["query_types"]])

    def test_connection_sources(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
    ) -> None:
        resp = control_api_sync_client.get(
            url=f"/api/v1/connections/{saved_connection_id}/info/sources",
            headers=bi_headers,
        )
        assert resp.status_code == 200, resp.json
        resp_data = resp.json
        assert "sources" in resp_data, resp_data
        assert isinstance(resp_data["sources"], list), resp_data

    def test_create_connections__query_params_in_db_name__error(
        self,
        control_api_sync_client: SyncHttpClientBase,
        saved_connection_id: str,
        bi_headers: Optional[dict[str, str]],
        connection_params: dict,
    ) -> None:
        if "db_name" not in connection_params:
            pytest.skip("No db_name field in schema")

        # arrange
        connection_params = connection_params.copy()
        connection_params["db_name"] = "db1?sslmode=required"
        data = dict(
            name=f"{self.conn_type.name} conn {uuid.uuid4()}",
            type=self.conn_type.name,
            **connection_params,
        )

        # act
        resp = control_api_sync_client.post(
            "/api/v1/connections",
            content_type="application/json",
            data=json.dumps(data),
            headers=bi_headers,
        )

        # assert
        assert resp.status_code == 400
        assert resp.json == {"db_name": ["There must be no query params in field db_name, found: db1?sslmode=required"]}
