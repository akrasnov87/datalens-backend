from dl_api_lib_testing.connector.connection_suite import DefaultConnectorConnectionTestSuite

from dl_connector_trino_tests.db.api.base import TrinoConnectionTestBase


class TestTrinoConnection(TrinoConnectionTestBase, DefaultConnectorConnectionTestSuite):
    pass
