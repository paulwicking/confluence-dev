import pytest
# import confluence
from confluence import confluence
from confluence import scroll


@pytest.fixture(scope='module')
def conf():
    test_conf = confluence.Confluence(profile='vizrt-test')
    yield test_conf

    # Teardown
    test_conf.connection.close()


@pytest.fixture(scope='module')
def versions(conf):
    version = scroll.ScrollVersions(conf)
    yield version


def test_get_all_attributes_and_values_returns_a_list(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert isinstance(result, list)


def test_get_all_attributes_and_values_list_contains_dict(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert isinstance(result[0], dict)


def test_get_all_attributes_and_values_dict_contains_id_key(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert 'id' in result[0]


def test_get_all_attributes_and_values_dict_contains_name_key(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert 'name' in result[0]


def test_get_all_attributes_and_values_dict_contains_values_key(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert 'values' in result[0]
