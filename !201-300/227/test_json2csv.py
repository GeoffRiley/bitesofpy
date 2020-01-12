import csv
from json.decoder import JSONDecodeError
from urllib.request import urlretrieve

import pytest
from json2csv import convert_to_csv, EXCEPTION, TMP

mount_data = (
    'https://bites-data.s3.us-east-2.amazonaws.com/'
    'mount-data{}.json'
)

mount1_expected = [
    ['creatureId', 'icon', 'isAquatic', 'isFlying', 'isGround', 'isJumping',
     'itemId', 'name', 'qualityId', 'spellId'],
    ['32158', 'ability_mount_drake_blue', 'False', 'True', 'True', 'False',
     '44178', 'Albino Drake', '4', '60025'],
    ['63502', 'ability_mount_hordescorpionamber', 'True', 'False', 'True',
     'True', '85262', 'Amber Scorpion', '4', '123886'],
    ['24487', 'ability_mount_warhippogryph', 'False', 'True', 'True', 'False',
     '45725', 'Argent Hippogryph', '4', '232412'],
]

mount2_expected = [
    ['creatureId', 'icon', 'isAquatic', 'isFlying', 'isGround', 'isJumping',
     'itemId', 'name', 'qualityId', 'spellId'],
    ['71381', 'ability_mount_dragonhawkarmorallliance', 'False', 'True',
     'True', 'False', '98259', 'Armored Blue Dragonhawk', '4', '142478'],
    ['304', 'spell_nature_swiftness', 'True', 'False', 'True', 'True', '0',
     'Felsteed', '1', '5784'],
    ['119386', 'inv_warlockmount', 'False', 'True', 'True', 'False', '0',
     "Netherlord's Chaotic Wrathsteed", '1', '232412'],
]


@pytest.mark.parametrize("file_no, expected, exception", [
    (1, mount1_expected, False),
    (2, mount2_expected, False),
    (3, None, True),
])
def test_json2csv(file_no, expected, exception, capfd):
    mount_json = TMP / f'mount{file_no}.json'
    mount_csv = TMP / f'mount{file_no}.csv'

    urlretrieve(mount_data.format(file_no), mount_json)

    if exception:
        with pytest.raises(JSONDecodeError) as exc:
            convert_to_csv(mount_json)
            assert 'Invalid control character' in str(exc)

        # testing you actually caught the exception!
        output = capfd.readouterr()[0].strip()
        assert output == EXCEPTION
        return

    convert_to_csv(mount_json)
    with open(mount_csv) as csv_file:
        actual = list(csv.reader(csv_file))
        assert actual == expected
