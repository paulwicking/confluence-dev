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
def versions():
    version = scroll.ScrollVersions()
    yield version


def test_get_all_attributes_and_values_returns_a_list(conf, versions):
    result = versions.get_all_available_attributes_and_values('VAE')
    assert isinstance(result, list)


def test_get_all_attributes_and_values_list_contains_dict(conf, versions):
    result = conf.get_all_available_attributes_and_values('VAE')
    assert isinstance(result[0], dict)


def test_get_all_attributes_and_values_dict_contains_id_key(conf, versions):
    result = conf.connection.get(conf.base_url + '/rest/scroll-versions/1.0/attribute/VAE').json()
    assert 'id' in result[0]


def test_get_all_attributes_and_values_dict_contains_name_key(conf, versions):
    result = conf.connection.get(conf.base_url + '/rest/scroll-versions/1.0/attribute/VAE').json()
    assert 'name' in result[0]


def test_get_all_attributes_and_values_dict_contains_values_key(conf, versions):
    result = conf.connection.get(conf.base_url + '/rest/scroll-versions/1.0/attribute/VAE').json()
    assert 'values' in result[0]
