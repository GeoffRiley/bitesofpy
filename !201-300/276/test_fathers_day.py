from fathers_day import get_father_days, generate_father_day_planning

CALENDAR_OUTPUT = """February 23
- Russia

March 19
- Andora
- Bolivia
- Honduras
- Italy
- Liechtenstein
- Portugal
- Spain

May 10
- Romania

May 21
- Germany

June 7
- Austria
- Belgium

June 14
- U.S.
- Canada
- U.K.

June 17
- El Salvador
- Guatemala

June 21
- Egypt
- Jordan
- Lebanon
- Syria
- Uganda

June 23
- Nicaragua
- Poland

August 9
- Samoa
- Brazil

September 6
- Fiji
- New Guinea
- Australia
- New Zealand

November 8
- Estonia
- Finland
- Iceland
- Norway
- Sweden"""


def test_get_father_days_default():
    father_days = get_father_days()
    assert len(father_days) == 12
    number_countries = sum(len(val) for val in father_days.values())
    assert number_countries == 35
    assert father_days['June 14'] == ['U.S.', 'Canada', 'U.K.']
    assert father_days['March 19'] == [
        'Andora', 'Bolivia', 'Honduras', 'Italy',
        'Liechtenstein', 'Portugal', 'Spain']
    assert father_days['June 23'] == ['Nicaragua', 'Poland']
    assert father_days['August 9'] == ['Samoa', 'Brazil']
    assert father_days['June 7'] == ['Austria', 'Belgium']
    assert father_days['May 21'] == ['Germany']


def test_get_father_days_other_years():
    father_days = get_father_days(year=2021)
    # changing dates
    assert father_days['June 20'] == ['U.S.', 'Canada', 'U.K.']
    assert father_days['August 8'] == ['Samoa', 'Brazil']
    assert father_days['May 13'] == ['Germany']
    assert father_days['June 13'] == ['Austria', 'Belgium']
    father_days = get_father_days(year=2022)
    assert father_days['May 26'] == ['Germany']
    assert father_days['June 12'] == ['Austria', 'Belgium']
    # remains the same
    assert father_days['March 19'] == [
        'Andora', 'Bolivia', 'Honduras', 'Italy',
        'Liechtenstein', 'Portugal', 'Spain']


def test_generate_father_day_planning(capfd):
    generate_father_day_planning()
    actual = capfd.readouterr()[0]
    assert actual.strip() == CALENDAR_OUTPUT
