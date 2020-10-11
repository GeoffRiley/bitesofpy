from nested_list_extract import extract_ipv4


def test_empty_list():
    assert extract_ipv4([]) == []


def test_flat_list_no_match():
    assert extract_ipv4(['ip']) == []


def test_nested_list_no_match():
    assert extract_ipv4([['ip', 'mask']]) == []


def test_nested_list_no_ip():
    assert extract_ipv4([['TEST', ['ip', [None], 'mask', ['24'], 'type', ['ip_mask']], 'id']]) == []


def test_nested_list_not_an_ip():
    assert extract_ipv4([['TEST', ['ip', ['"not.an.ip.address"'], 'mask', ['24'], 'type', ['ip_mask']], 'id']]) == []


def test_nested_list_no_mask():
    assert extract_ipv4([['TEST', ['ip', ['"1.1.1.0"'], 'mask', [None], 'type', ['ip_mask']], 'id']]) == []


def test_flat_list():
    assert extract_ipv4(['ip', ['"172.16.0.0"'], 'mask', ['12'], 'type', ['ip_mask']]) == [('172.16.0.0', '12')]


def test_nested_list():
    assert extract_ipv4(
        ['TEST', 'parent', [], 'uuid', '"khk-yyas4h-323223-wewe-343er-3434-www"', 'display_name', '"services"', 'IPV4',
         [['ip', ['"192.168.1.0"'], 'mask', ['24'], 'type', ['ip_mask']],
          ['ip', ['"10.0.0.0"'], 'mask', ['8'], 'type', ['ip_mask']]]]) == [('192.168.1.0', '24'), ('10.0.0.0', '8')]


def test_deeply_nested_list():
    assert extract_ipv4([['TEST', ['parent', [], 'uuid', ['"khk-yyas4h-323223-wewe-343er-3434-www"'], 'display_name',
                                   ['"services"'], 'IPV4', [[['ip', ['"1.1.1.0"'], 'mask', ['20'], 'type', ['ip_mask']],
                                                             ['ip', ['"2.2.2.2"'], 'mask', ['32'], 'type',
                                                              ['ip_mask']]]]]]]) == [('1.1.1.0', '20'),
                                                                                     ('2.2.2.2', '32')]
