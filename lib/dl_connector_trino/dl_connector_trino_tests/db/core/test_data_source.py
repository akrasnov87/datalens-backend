import pytest

from dl_constants.enums import (
    RawSQLLevel,
    UserDataType,
)
from dl_core.data_source_spec.sql import (
    StandardSchemaSQLDataSourceSpec,
    SubselectDataSourceSpec,
)
from dl_core_testing.database import DbTable
from dl_core_testing.fixtures.sample_tables import TABLE_SPEC_SAMPLE_SUPERSTORE
from dl_core_testing.testcases.data_source import DefaultDataSourceTestClass

from dl_connector_trino.core.constants import (
    SOURCE_TYPE_TRINO_SUBSELECT,
    SOURCE_TYPE_TRINO_TABLE,
)
from dl_connector_trino.core.data_source import (
    TrinoSubselectDataSource,
    TrinoTableDataSource,
)
from dl_connector_trino.core.us_connection import ConnectionTrino
from dl_connector_trino_tests.db.core.base import BaseTrinoTestClass


class TestTrinoTableDataSource(
    BaseTrinoTestClass,
    DefaultDataSourceTestClass[
        ConnectionTrino,
        StandardSchemaSQLDataSourceSpec,
        TrinoTableDataSource,
    ],
):
    DSRC_CLS = TrinoTableDataSource

    @pytest.fixture(scope="class")
    def initial_data_source_spec(self, sample_table: DbTable) -> StandardSchemaSQLDataSourceSpec:
        dsrc_spec = StandardSchemaSQLDataSourceSpec(
            source_type=SOURCE_TYPE_TRINO_TABLE,
            db_name=sample_table.db.name,
            schema_name=sample_table.schema,
            table_name=sample_table.name,
        )
        return dsrc_spec

    def get_expected_simplified_schema(self) -> list[tuple[str, UserDataType]]:
        return list(TABLE_SPEC_SAMPLE_SUPERSTORE.table_schema)


class TestTrinoSubselectDataSource(
    BaseTrinoTestClass,
    DefaultDataSourceTestClass[
        ConnectionTrino,
        SubselectDataSourceSpec,
        TrinoSubselectDataSource,
    ],
):
    DSRC_CLS = TrinoSubselectDataSource

    raw_sql_level = RawSQLLevel.subselect

    @pytest.fixture(scope="class")
    def initial_data_source_spec(self, sample_table: DbTable) -> SubselectDataSourceSpec:
        dsrc_spec = SubselectDataSourceSpec(
            source_type=SOURCE_TYPE_TRINO_SUBSELECT,
            subsql=f"SELECT * FROM {sample_table.db.name}.{sample_table.schema}.{sample_table.name}",
        )
        return dsrc_spec

    def get_expected_simplified_schema(self) -> list[tuple[str, UserDataType]]:
        return list(TABLE_SPEC_SAMPLE_SUPERSTORE.table_schema)
