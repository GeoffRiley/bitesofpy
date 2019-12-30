import pytest

from permissions import get_octal_from_file_permission


@pytest.mark.parametrize("input_arg, expected", [
    ('-----x-w-', '012'), ('-----x-wx', '013'), ('-----xr--', '014'),
    ('-----xr-x', '015'), ('-----xrw-', '016'), ('-----xrwx', '017'),
    ('----w--wx', '023'), ('----w-r--', '024'), ('----w-r-x', '025'),
    ('----w-rw-', '026'), ('----w-rwx', '027'), ('----wxr--', '034'),
    ('----wxr-x', '035'), ('----wxrw-', '036'), ('----wxrwx', '037'),
    ('---r--r-x', '045'), ('---r--rw-', '046'), ('---r--rwx', '047'),
    ('---r-xrw-', '056'), ('---r-xrwx', '057'), ('---rw-rwx', '067'),
    ('--x-w--wx', '123'), ('--x-w-r--', '124'), ('--x-w-r-x', '125'),
    ('--x-w-rw-', '126'), ('--x-w-rwx', '127'), ('--x-wxr--', '134'),
    ('--x-wxr-x', '135'), ('--x-wxrw-', '136'), ('--x-wxrwx', '137'),
    ('--xr--r-x', '145'), ('--xr--rw-', '146'), ('--xr--rwx', '147'),
    ('--xr-xrw-', '156'), ('--xr-xrwx', '157'), ('--xrw-rwx', '167'),
    ('-w--wxr--', '234'), ('-w--wxr-x', '235'), ('-w--wxrw-', '236'),
    ('-w--wxrwx', '237'), ('-w-r--r-x', '245'), ('-w-r--rw-', '246'),
    ('-w-r--rwx', '247'), ('-w-r-xrw-', '256'), ('-w-r-xrwx', '257'),
    ('-w-rw-rwx', '267'), ('-wxr--r-x', '345'), ('-wxr--rw-', '346'),
    ('-wxr--rwx', '347'), ('-wxr-xrw-', '356'), ('-wxr-xrwx', '357'),
    ('-wxrw-rwx', '367'), ('r--r-xrw-', '456'), ('r--r-xrwx', '457'),
    ('r--rw-rwx', '467'), ('r-xrw-rwx', '567'),
])
def test_octal_results_for_different_rwx_combinations(input_arg, expected):
    assert get_octal_from_file_permission(input_arg) == expected
