import json
import os
from pathlib import Path
from urllib.request import urlretrieve

filename = "my_code.json"
url = "https://bites-data.s3.us-east-2.amazonaws.com/{filename}"
tmp = Path(os.getenv("TMP", "/tmp"))
json_input_file = tmp / filename

if not json_input_file.exists():
    urlretrieve(url.format(filename=filename), json_input_file)


def get_json_data():
    with open(json_input_file) as file_in:
        return json.load(file_in)


json_data = get_json_data()


def get_passing_code(json_data=json_data):
    """Get all passing code and write the code for each bite to individual files.
       Outut file names should be the bite name and number with a .py extension,
       but not including the description.  For example, if the bite name is
       'Bite 124. Marvel data analysis' the output file names should be Bite124.py.
       Remove any/all spaces from the file name.
       Write to /tmp (tmp variable).
    """
    for bite in json_data['bites']:
        bite_name = bite['bite'].split(' ', 2)
        assert bite_name[0] == 'Bite'
        fn = tmp / (''.join(bite_name[:2]) + 'py')
        with open(fn, 'wb') as f:
            f.write(bytes(bite['passing_code'].encode('utf8')))
