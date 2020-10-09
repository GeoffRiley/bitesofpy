import pytest

from domains import get_common_domains, get_most_common_domains


@pytest.fixture(scope="module")
def common_domains():
    return list(get_common_domains())


def test_get_common_domains(common_domains):
    assert len(common_domains) == 100
    first_3 = ['gmail.com', 'yahoo.com', 'hotmail.com']
    last_3 = ['live.ca', 'aim.com', 'bigpond.net.au']
    assert common_domains[:3] == first_3
    assert common_domains[-3:] == last_3


@pytest.mark.parametrize("emails, expected", [
    (["a@gmail.com", "b@pybit.es", "c@pybit.es", "d@domain.de"],
     [('pybit.es', 2), ('domain.de', 1)]),
    (["a@hotmail.com", "b@gmail.com"], []),
    (["a@hotmail.com", "b@hotmail.se",
      "c@paris.com", "d@paris.com", "e@hotmail.it"],
     [('paris.com', 2), ('hotmail.se', 1)]),
    (["a@gmail.es", "b@googlemail.com", "c@somedomain.com",
      "d@somedomain.com", "e@somedomain.com", "f@hotmail.fr"],
     [('somedomain.com', 3), ('gmail.es', 1)]),
])
def test_get_most_common_domains(common_domains, emails, expected):
    assert get_most_common_domains(emails, common_domains) == expected
