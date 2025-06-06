from dl_api_lib_testing.initialization import initialize_api_lib_test
from dl_core_testing.database import (
    CoreDbConfig,
    CoreDbDispenser,
)
from dl_db_testing.database.engine_wrapper import DbEngineConfig
from dl_formula_testing.forced_literal import forced_literal_use

from dl_connector_oracle.core.constants import CONNECTION_TYPE_ORACLE
from dl_connector_oracle_tests.db.config import (
    API_TEST_CONFIG,
    SYSDBA_URL,
    SYSDBA_URL_SSL,
    fetch_ca_certificate,
    make_ssl_engine_params,
)


def pytest_configure(config):  # noqa
    initialize_api_lib_test(pytest_config=config, api_test_config=API_TEST_CONFIG)
    initialize_db()


def initialize_db():
    # Granting of priveleges con only be done when connecting as sydba
    db_dispenser = CoreDbDispenser()
    sysdba_db_config = CoreDbConfig(engine_config=DbEngineConfig(url=SYSDBA_URL), conn_type=CONNECTION_TYPE_ORACLE)
    sysdba_db = db_dispenser.get_database(db_config=sysdba_db_config)
    sysdba_db.execute("GRANT SELECT ON sys.V_$SESSION TO datalens")

    sysdba_db_ssl_config = CoreDbConfig(
        engine_config=DbEngineConfig(
            url=SYSDBA_URL_SSL,
            engine_params=make_ssl_engine_params(fetch_ca_certificate()),
        ),
        conn_type=CONNECTION_TYPE_ORACLE,
    )
    sysdba_db_ssl = db_dispenser.get_database(db_config=sysdba_db_ssl_config)
    sysdba_db_ssl.execute("GRANT SELECT ON sys.V_$SESSION TO datalens")


__all__ = (
    # auto-use fixtures:
    "forced_literal_use",
)
