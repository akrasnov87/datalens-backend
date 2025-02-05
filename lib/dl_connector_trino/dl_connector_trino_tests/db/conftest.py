from dl_api_lib_testing.initialization import initialize_api_lib_test

from dl_connector_trino_tests.db.config import API_TEST_CONFIG


def pytest_configure(config):
    initialize_api_lib_test(pytest_config=config, api_test_config=API_TEST_CONFIG)
