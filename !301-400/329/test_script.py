from script import snake_case_keys


def test_empty_object():
    data = {}
    assert snake_case_keys(data) == data


def test_no_transform():
    data = {"star": "wars"}
    assert snake_case_keys(data) == data


def test_single_key_transform():
    data = {"starWars": "is awesome"}
    expected = {"star_wars": "is awesome"}
    assert snake_case_keys(data) == expected


def test_leading_capital():
    data = {"DarthVader": "James Earl Jones"}
    expected = {"darth_vader": "James Earl Jones"}
    assert snake_case_keys(data) == expected


def test_snake_case_stays():
    data = {"darth_vader": "James Earl Jones"}
    assert snake_case_keys(data) == data


def test_transform_kebab_case():
    data = {"darth-vader": "James Earl Jones"}
    expected = {"darth_vader": "James Earl Jones"}
    assert snake_case_keys(data) == expected


def test_acronyms():
    data = {"numTIEFighters": 1e5}
    expected = {"num_t_i_e_fighters": 1e5}
    assert snake_case_keys(data) == expected


def test_single_digit():
    data = {"emperorsNumber2": "Darth Vader"}
    expected = {"emperors_number_2": "Darth Vader"}
    assert snake_case_keys(data) == expected


def test_multi_digit():
    data = {"executeOrder66": "yes sir!"}
    expected = {"execute_order_66": "yes sir!"}
    assert snake_case_keys(data) == expected


def test_multi_first_level_keys():
    data = {"firstName": "Han", "lastName": "Solo"}
    expected = {"first_name": "Han", "last_name": "Solo"}
    assert snake_case_keys(data) == expected


def test_nested_object():
    data = {
        "darthVader": {
            "firstName": "Anakin",
            "lastName": "Skywalker",
            "appearance": {
                "helmetColor": "black",
                "armorColor": "black",
                "capeColor": "black",
            },
        }
    }
    expected = {
        "darth_vader": {
            "first_name": "Anakin",
            "last_name": "Skywalker",
            "appearance": {
                "helmet_color": "black",
                "armor_color": "black",
                "cape_color": "black",
            },
        }
    }
    assert snake_case_keys(data) == expected


def test_nested_list():
    data = {
        "firstName": "Anakin",
        "lastName": "Skywalker",
        "children": [{"firstName": "Luke"},
                     {"firstName": "Leia"}],
    }
    expected = {
        "first_name": "Anakin",
        "last_name": "Skywalker",
        "children": [{"first_name": "Luke"},
                     {"first_name": "Leia"}],
    }
    assert snake_case_keys(data) == expected


def test_list_in_list():
    data = {
        "random": [
            "Luke",
            [
                "blowing up the death star",
                {"skillName": "bulls-eye womprats",
                 "skillParameters": "with my T47"},
            ],
        ]
    }
    expected = {
        "random": [
            "Luke",
            [
                "blowing up the death star",
                {"skill_name": "bulls-eye womprats",
                 "skill_parameters": "with my T47"},
            ],
        ]
    }
    assert snake_case_keys(data) == expected
