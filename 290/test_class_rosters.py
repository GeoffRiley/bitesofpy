import pytest

from class_rosters import class_rosters

full = """
17409,"Matheson, Rick",,,,,,,,,,
36283,"Jones, Tom",SCI09-4 - SU,MATH09-2 - PH,TA09-1 - AB,IS09-4 - LM,SCI09-3 - NdN,MATH09-2 - RB,DE09-3 - KmQ,ENG09-3 - KaR,PE09-3 - PS
99415,"Blake, Arnold",,,,,,,,,,
"""  # noqa E501
partial = """
17409,"Jones, Tom",,,,,,,,,,
17409,"Matheson, Rick",,IS09-1 - BR,,SCI09-4 - SU,MATH09-2 - RB,,ENG09-4 - LE,,PE09-1 - MR,
99415,"Blake, Arnold",,,,,,,,,,
"""  # noqa E501
empty = """
99415,"Blake, Arnold",,,,,,,,,,
21692,"Prest, Phil",,,,,,,,,,
36283,"Jones, Tom",,,,,,,,,,
"""  # noqa E501


@pytest.mark.parametrize("content, expected", [
    (full, ['SCI09-4,2020,36283',
            'MATH09-2,2020,36283',
            'TA09-1,2020,36283',
            'IS09-4,2020,36283',
            'SCI09-3,2020,36283',
            'MATH09-2,2020,36283',
            'DE09-3,2020,36283',
            'ENG09-3,2020,36283',
            'PE09-3,2020,36283']),
    (partial, ['IS09-1,2020,17409',
               'SCI09-4,2020,17409',
               'MATH09-2,2020,17409',
               'ENG09-4,2020,17409',
               'PE09-1,2020,17409']),
    (empty, []),
])
def test_class_rosters(content, expected, tmp_path):
    csvfile = tmp_path / "content"
    csvfile.write_text(content.lstrip())
    actual = class_rosters(csvfile)
    assert actual == expected
