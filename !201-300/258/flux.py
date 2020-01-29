from pandas import read_csv

XYZ = "https://bites-data.s3.us-east-2.amazonaws.com/xyz.csv"
THRESHOLDS = (5000, 0.05)


def calculate_flux(XYZ: str) -> list:
    """Read the data in from xyz.csv
    add two new columns, one to calculate dollar flux,
    and the other to calculate percentage flux
    return as a list of tuples
    """
    data = read_csv(XYZ)
    cols = list(data.columns)
    data['flux'] = data[cols[1]] - data[cols[2]]
    data['percent'] = data['flux'] / data[cols[2]]
    return list(data.itertuples(index=False, name=None))


def identify_flux(xyz: list) -> list:
    """Load the list of tuples, iterate through
    each item and determine if it is above both
    thresholds. if so, add to the list
    """
    flagged_lines = []
    for acc in xyz:
        if abs(acc[3]) > THRESHOLDS[0] and abs(acc[4]) > THRESHOLDS[1]:
            flagged_lines.append(acc)
    return flagged_lines
