from __future__ import annotations

import logging
import typing
from typing import Optional

import attr

from dl_api_commons.base_models import RequestContextInfo
from dl_api_lib.i18n.localizer import Translatable
from dl_constants.enums import DataSourceRole
from dl_core import us_dataset
from dl_core.components.accessor import DatasetComponentAccessor
from dl_core.data_source.collection import DataSourceCollectionFactory
from dl_core.dataset_capabilities import DatasetCapabilities
from dl_core.exc import EntityUsageNotAllowed
from dl_core.services_registry.entity_checker import EntityUsageChecker
from dl_core.us_connection_base import ConnectionBase
from dl_i18n.localizer_base import Localizer


if typing.TYPE_CHECKING:
    from dl_core.us_manager.us_manager import USManagerBase


LOGGER = logging.getLogger(__name__)


@attr.s
class PublicEnvEntityUsageChecker(EntityUsageChecker):
    def ensure_dataset_can_be_used(
        self,
        rci: RequestContextInfo,
        dataset: us_dataset.Dataset,
        us_manager: USManagerBase,
        localizer: Optional[Localizer] = None,
    ) -> None:
        ds_accessor = DatasetComponentAccessor(dataset=dataset)
        dsrc_coll_factory = DataSourceCollectionFactory(us_entry_buffer=us_manager.get_entry_buffer())
        capabilities = DatasetCapabilities(dataset=dataset, dsrc_coll_factory=dsrc_coll_factory)
        LOGGER.info("Checking if dataset %s can be used in public env", dataset.uuid)
        main_source_role = capabilities.resolve_source_role()
        LOGGER.info("Dataset source role is %s", main_source_role)

        if main_source_role == DataSourceRole.materialization:
            LOGGER.info("Dataset source role is %s. Usage is allowed", main_source_role)
            return
        elif main_source_role == DataSourceRole.origin:
            LOGGER.info("Dataset source role is %s. Underlying connections will be checked", main_source_role)
            dsrc_coll_spec_list = ds_accessor.get_data_source_coll_spec_list()

            dsrc_coll_list = [
                dsrc_coll_factory.get_data_source_collection(
                    spec=dsrc_coll_spec,
                    dataset_parameter_values=ds_accessor.get_parameter_values(),
                    dataset_template_enabled=ds_accessor.get_template_enabled(),
                )
                for dsrc_coll_spec in dsrc_coll_spec_list
            ]

            effective_data_source_list = [dsrc_coll.get_strict() for dsrc_coll in dsrc_coll_list]
            conn_set = {dsrc.connection for dsrc in effective_data_source_list}
            LOGGER.info(
                "Dataset has %d data source, %d connections used",
                len(effective_data_source_list),
                len(conn_set),
            )

            conn_validation_exc_map = {}

            for conn in conn_set:
                try:
                    self.ensure_data_connection_can_be_used(rci, conn)
                except EntityUsageNotAllowed as conn_not_allowed_exc:
                    assert conn.uuid
                    conn_validation_exc_map[conn.uuid] = dict(
                        exc=str(conn_not_allowed_exc),
                        conn_type=conn.conn_type.value,
                    )

            if len(conn_validation_exc_map) == 0:
                LOGGER.info("All connections are allowed to be used in public env")
                return
            else:
                nonpublic_conn_ids = list()
                nonpublic_conn_types = list()

                for conn_id, nonpublic_conn in conn_validation_exc_map.items():
                    conn_type, exc = nonpublic_conn["conn_type"], nonpublic_conn["exc"]
                    nonpublic_conn_ids.append(conn_id)
                    nonpublic_conn_types.append(conn_type)
                    LOGGER.info("Connection %s is not allowed to be used in public env: %s", conn_id, exc)

                if localizer:
                    error_msg = localizer.translate(Translatable("warning-publication-not-allowed")).format(
                        conn_type=", ".join(nonpublic_conn_types), conn_id=", ".join(nonpublic_conn_ids)
                    )
                else:
                    error_msg = "The publication of this object or some of its dependencies is not allowed"

                raise EntityUsageNotAllowed(error_msg)
        else:
            raise EntityUsageNotAllowed(f"Unexpected data source role resolved for dataset {dataset.uuid}")

    def ensure_data_connection_can_be_used(self, rci: RequestContextInfo, conn: ConnectionBase) -> None:
        LOGGER.info("Checking if connection %s %s can be used in public env", conn.conn_type, conn.uuid)
        if conn.allow_public_usage:
            return
        raise EntityUsageNotAllowed(f"Connection type {conn.conn_type.value} can not be used in public dataset")
