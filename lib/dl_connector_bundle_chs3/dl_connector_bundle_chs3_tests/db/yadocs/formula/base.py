import pytest

from dl_formula_testing.testcases.base import FormulaConnectorTestBase

from dl_connector_bundle_chs3.chs3_yadocs.formula.constants import YaDocsFileS3Dialect as D
from dl_connector_bundle_chs3_tests.db.config import DB_CH_URL
from dl_connector_clickhouse.db_testing.engine_wrapper import ClickhouseDbEngineConfig


class YaDocsTestBase(FormulaConnectorTestBase):
    dialect = D.YADOCS
    engine_config_cls = ClickhouseDbEngineConfig
    supports_arrays = True
    supports_uuid = True

    @pytest.fixture(scope="class")
    def db_url(self) -> str:
        return DB_CH_URL
