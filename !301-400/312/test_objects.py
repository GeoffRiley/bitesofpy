import pytest

from objects import score_objects


@pytest.mark.parametrize("arg, expected", [
    pytest.param(['none', '1', 'nonsense'], 0, id="nothing_matches"),
    pytest.param(['random'], 3, id="one_module"),
    pytest.param(['raise', 'random'], 5, id="one_keyword_one_module"),
    pytest.param(['any', 'all', 'max'], 3, id="three_builtins"),
    pytest.param(['and', 'if', 'is'], 6, id="three_keywords"),
    pytest.param(['builtins', 'numbers', 'os'], 9, id="three_modules"),
    pytest.param(['zip', 'itertools'], 4, id="one_builtin_one_module"),
    pytest.param(['pytest', 'os'], 6, id="external_and_stdlib"),
    pytest.param(['re', 'pathlib'], 6, id="two_modules"),
    pytest.param(['objects'], 3, id="import_self"),
    pytest.param(['sys', 'global'], 5, id="one_module_one_keyword"),
    pytest.param(['json', 'dict', 're'], 7, id="two_modules_one_builtin"),
    pytest.param(['hashlib', 'base64', 'nonlocal'], 8, id="two_modules_one_keyword"),
    pytest.param(['global', '4', 'sys.exit'], 2, id="one_keyword_and_nomatches"),
    pytest.param(['None', 'False', 'True'], 9, id="three_keywords_and_builtins"),
])
def test_score_objects(arg, expected):
    assert score_objects(arg) == expected
