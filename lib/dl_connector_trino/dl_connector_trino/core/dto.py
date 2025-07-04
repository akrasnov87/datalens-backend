from typing import Optional

import attr

from dl_core.connection_models.dto_defs import ConnDTO

from dl_connector_trino.core.constants import (
    CONNECTION_TYPE_TRINO,
    TrinoAuthType,
)


@attr.s(frozen=True)
class TrinoConnDTO(ConnDTO):
    conn_type = CONNECTION_TYPE_TRINO
    host: str = attr.ib(kw_only=True)
    port: int = attr.ib(kw_only=True)
    username: str = attr.ib(kw_only=True)
    auth_type: TrinoAuthType = attr.ib(kw_only=True)
    password: Optional[str] = attr.ib(repr=False, kw_only=True, default=None)
    jwt: Optional[str] = attr.ib(repr=False, kw_only=True, default=None)
    ssl_enable: bool = attr.ib(kw_only=True, default=False)
    ssl_ca: Optional[str] = attr.ib(kw_only=True, default=None)

    def conn_reporting_data(self) -> dict:
        return super().conn_reporting_data() | dict(
            host=self.host,
        )
