from __future__ import annotations

import abc
from typing import (
    TYPE_CHECKING,
    AbstractSet,
    Callable,
    ClassVar,
    Optional,
    Type,
)

from sqlalchemy.orm import Query

from dl_constants.enums import SourceBackendType
from dl_core.connections_security.base import ConnSecuritySettings
from dl_core.connectors.base.data_source_migration import (
    DataSourceMigrator,
    DefaultDataSourceMigrator,
)
from dl_core.connectors.base.lifecycle import (
    ConnectionLifecycleManager,
    DefaultConnectionLifecycleManager,
)
from dl_core.connectors.base.query_compiler import QueryCompiler
from dl_core.connectors.base.schema_migration import (
    ConnectionSchemaMigration,
    DefaultConnectionSchemaMigration,
)
from dl_core.connectors.settings.primitives import ConnectorSettingsDefinition
from dl_core.data_source.base import DataSource
from dl_core.data_source_spec.base import DataSourceSpec
from dl_core.us_manager.storage_schemas.data_source_spec_base import DataSourceSpecStorageSchema
from dl_dashsql.literalizer import (
    DashSQLParamLiteralizer,
    DefaultDashSQLParamLiteralizer,
)


if TYPE_CHECKING:
    from marshmallow import Schema
    from sqlalchemy.types import TypeEngine

    from dl_constants.enums import (
        ConnectionType,
        DataSourceType,
    )
    from dl_core.connection_executors.adapters.common_base import CommonBaseDirectAdapter
    from dl_core.connection_executors.async_base import AsyncConnExecutorBase
    from dl_core.connection_executors.common_base import ConnExecutorBase
    from dl_core.reporting.notifications import BaseNotification
    from dl_core.us_connection_base import ConnectionBase
    from dl_type_transformer.native_type import GenericNativeType
    from dl_type_transformer.type_transformer import TypeTransformer


class CoreSourceDefinition(abc.ABC):
    source_type: ClassVar[DataSourceType]
    source_cls: ClassVar[Type[DataSource]] = DataSource  # type: ignore  # 2024-01-30 # TODO: Can only assign concrete classes to a variable of type "type[DataSource]"  [type-abstract]
    source_spec_cls: ClassVar[Type[DataSourceSpec]] = DataSourceSpec
    us_storage_schema_cls: ClassVar[Type[DataSourceSpecStorageSchema]] = DataSourceSpecStorageSchema


class CoreConnectionDefinition(abc.ABC):
    conn_type: ClassVar[ConnectionType]
    connection_cls: ClassVar[Type[ConnectionBase]]
    us_storage_schema_cls: ClassVar[Optional[Type[Schema]]] = None
    type_transformer_cls: ClassVar[Type[TypeTransformer]]  # TODO: Move to CoreBackendDefinition
    sync_conn_executor_cls: ClassVar[Optional[Type[ConnExecutorBase]]] = None
    async_conn_executor_cls: ClassVar[Optional[Type[AsyncConnExecutorBase]]] = None
    lifecycle_manager_cls: ClassVar[Type[ConnectionLifecycleManager]] = DefaultConnectionLifecycleManager
    schema_migration_cls: ClassVar[Type[ConnectionSchemaMigration]] = DefaultConnectionSchemaMigration
    dialect_string: ClassVar[str]
    data_source_migrator_cls: ClassVar[Type[DataSourceMigrator]] = DefaultDataSourceMigrator
    settings_definition: ClassVar[Optional[Type[ConnectorSettingsDefinition]]] = None
    custom_dashsql_key_names: frozenset[str] = frozenset()
    allow_export: ClassVar[bool] = False


class CoreBackendDefinition(abc.ABC):
    backend_type: ClassVar[SourceBackendType] = SourceBackendType.NONE
    compiler_cls: ClassVar[Type[QueryCompiler]] = QueryCompiler
    query_cls: ClassVar[Type[Query]] = Query
    dashsql_literalizer_cls: ClassVar[Type[DashSQLParamLiteralizer]] = DefaultDashSQLParamLiteralizer


class CoreConnector(abc.ABC):
    # others
    backend_definition: Type[CoreBackendDefinition]
    connection_definitions: ClassVar[tuple[Type[CoreConnectionDefinition], ...]] = ()
    source_definitions: ClassVar[tuple[Type[CoreSourceDefinition], ...]] = ()
    # TODO: Move to CoreBackendDefinition:
    sa_types: ClassVar[
        Optional[dict[tuple[SourceBackendType, GenericNativeType], Callable[[GenericNativeType], TypeEngine]]]
    ] = None
    rqe_adapter_classes: ClassVar[AbstractSet[Type[CommonBaseDirectAdapter]]] = frozenset()
    conn_security: ClassVar[AbstractSet[ConnSecuritySettings]] = frozenset()
    query_fail_exceptions: frozenset[Type[Exception]] = frozenset()
    notification_classes: ClassVar[tuple[Type[BaseNotification], ...]] = ()

    @classmethod
    def registration_hook(cls) -> None:
        """Do some non-standard stuff here. Think twice before implementing."""
        return
