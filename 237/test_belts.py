from urllib.request import urlretrieve

from belts import TMP, get_belts


def get_data(file_no=1, tmp=TMP):
    file_name = f'bite_scores{file_no}.json'
    file_path = TMP / file_name
    remote = 'https://bites-data.s3.us-east-2.amazonaws.com/'
    if not file_path.exists():
        urlretrieve(f'{remote}{file_name}',
                    file_path)
    return file_path


def test_data_set1():
    data = get_data(1)
    actual = get_belts(data)
    # py 3.7 we should be able to rely on ordering
    expected = {
        'white': 'January 23, 2018',
        'yellow': 'June 20, 2018',
        'orange': 'October 07, 2018',
        'green': 'April 08, 2019'
    }
    assert actual == expected


def test_data_set2():
    data = get_data(2)
    actual = get_belts(data)
    expected = {
        'white': 'January 06, 2018',
        'yellow': 'January 25, 2018',
        'orange': 'February 08, 2018',
        'green': 'March 15, 2018',
        'blue': 'April 29, 2018',
        'brown': 'July 13, 2018',
        'black': 'October 31, 2018',
        'paneled': 'March 01, 2019',
        'red': 'June 26, 2019'
    }
    assert actual == expected
