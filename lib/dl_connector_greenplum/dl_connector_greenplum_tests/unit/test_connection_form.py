import pytest

from dl_api_connector.i18n.localizer import CONFIGS as BI_API_CONNECTOR_CONFIGS
from dl_api_lib_testing.connection_form_base import (
    ConnectionFormTestBase,
    DatasourceTemplateConnectionFormTestMixin,
)

from dl_connector_greenplum.api.connection_form.form_config import GreenplumConnectionFormFactory
from dl_connector_greenplum.api.i18n.localizer import CONFIGS as BI_CONNECTOR_GREENPLUM_CONFIGS
from dl_connector_greenplum.core.settings import GreenplumConnectorSettings
from dl_connector_postgresql.api.i18n.localizer import CONFIGS as BI_CONNECTOR_POSTGRESQL_CONFIGS


class TestGreenplumConnectionForm(
    ConnectionFormTestBase,
    DatasourceTemplateConnectionFormTestMixin,
):
    CONN_FORM_FACTORY_CLS = GreenplumConnectionFormFactory
    TRANSLATION_CONFIGS = BI_API_CONNECTOR_CONFIGS + BI_CONNECTOR_GREENPLUM_CONFIGS + BI_CONNECTOR_POSTGRESQL_CONFIGS

    @pytest.fixture
    def connectors_settings(
        self,
        enable_datasource_template: bool,
    ) -> GreenplumConnectorSettings:
        return GreenplumConnectorSettings(
            ENABLE_DATASOURCE_TEMPLATE=enable_datasource_template,
        )
