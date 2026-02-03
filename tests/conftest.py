def pytest_configure(config):
    config.addinivalue_line('markers', 'integration: интеграционные тесты')
    config.addinivalue_line('markers', 'unit: unit-тесты')
