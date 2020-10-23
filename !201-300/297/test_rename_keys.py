from datetime import datetime

import pytest
from rename_keys import rename_keys


def fb(value):
    return str(value)


@pytest.mark.parametrize('test_input, expected', [
    ({}, {}),
    ({'user_name': 'jdoe'}, {'user_name': 'jdoe'}),
    ({'@user_name': 'jdoe'}, {'user_name': 'jdoe'}),
    ({'@user_name': 'jdoe', 1: 'one', 2: 'two', '@three': 3},
     {'user_name': 'jdoe', 1: 'one', 2: 'two', 'three': 3},),
    ({(True, False): '@Fizz@', (False, True): '@Buzz@', (True, True): '@FizzBizz@', (False, False): fb},
     {(True, False): '@Fizz@', (False, True): '@Buzz@', (True, True): '@FizzBizz@', (False, False): fb}),
    ({'@pii': {'name': {'@first_name': 'Jane', '@last_name': 'Doe'},
               '@address': [{'@city': 'London'}, {'city': 'Moscow'}],
               '@id': 12345,
               '@email': 'jane@example.com'}},
     {'pii': {'name': {'first_name': 'Jane', 'last_name': 'Doe'},
              'address': [{'city': 'London'}, {'city': 'Moscow'}],
              'id': 12345,
              'email': 'jane@example.com'}}),
    ({'@contentUrl': 'contentUrl',
      '@createdAt': datetime.strptime('2020-06-11T09:08:13Z', '%Y-%m-%dT%H:%M:%SZ'),
      '@defaultViewId': 'defaultViewId',
      '@encryptExtracts': False,
      '@id': 'id',
      '@name': 'Login',
      '@showTabs': True,
      '@size': 1,
      '@updatedAt': datetime.strptime('2020-07-20T06:41:34Z', '%Y-%m-%dT%H:%M:%SZ'),
      '@webpageUrl': 'webpageUrl',
      'dataAccelerationConfig': {'@accelerationEnabled': False},
      'owner': {'@id': 'id', '@name': 'name'},
      'project': {'@id': 'id', '@name': 'name'},
      'tags': {'tag': {'@label': 'label'}},
      'views': {'view': [{'@contentUrl': 'contentUrl',
                          '@createdAt': '2020-06-11T09:08:13Z',
                          '@id': 'id',
                          '@name': 'name',
                          '@updatedAt': '2020-07-20T06:41:34Z',
                          '@viewUrlName': 'Sheet1',
                          'tags': {'tag': {'@label': 'label'}}},
                         {'@contentUrl': 'contentUrl',
                          '@createdAt': '2020-06-11T09:08:13Z',
                          '@id': 'id',
                          '@name': 'name',
                          '@updatedAt': 'updatedAt',
                          '@viewUrlName': 'viewUrlName',
                          'tags': {'tag': {'@label': 'label'}}}]}},
     {'contentUrl': 'contentUrl',
      'createdAt': datetime(2020, 6, 11, 9, 8, 13),
      'dataAccelerationConfig': {'accelerationEnabled': False},
      'defaultViewId': 'defaultViewId',
      'encryptExtracts': False,
      'id': 'id',
      'name': 'Login',
      'owner': {'id': 'id', 'name': 'name'},
      'project': {'id': 'id', 'name': 'name'},
      'showTabs': True,
      'size': 1,
      'tags': {'tag': {'label': 'label'}},
      'updatedAt': datetime(2020, 7, 20, 6, 41, 34),
      'views': {'view': [{'contentUrl': 'contentUrl',
                          'createdAt': '2020-06-11T09:08:13Z',
                          'id': 'id',
                          'name': 'name',
                          'tags': {'tag': {'label': 'label'}},
                          'updatedAt': '2020-07-20T06:41:34Z',
                          'viewUrlName': 'Sheet1'},
                         {'contentUrl': 'contentUrl',
                          'createdAt': '2020-06-11T09:08:13Z',
                          'id': 'id',
                          'name': 'name',
                          'tags': {'tag': {'label': 'label'}},
                          'updatedAt': 'updatedAt',
                          'viewUrlName': 'viewUrlName'}]},
      'webpageUrl': 'webpageUrl'})
])
def test_rename_keys(test_input, expected):
    snapshot_before = repr(test_input)
    renamed = rename_keys(test_input)
    snapshot_after = repr(test_input)

    assert renamed == expected

    # make sure we're returning a new dict and the original dict was not modified in place
    assert test_input is not renamed
    assert snapshot_before == snapshot_after if '@' in snapshot_before else True
