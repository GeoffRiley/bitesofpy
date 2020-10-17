def class_rosters(input_file):
    """
        Read the input_file and modify the data
        according to the Bite description.
        Return a list holding one item per student
        per class, correctly formatted.
    """
    out = []
    with open(input_file, 'rt') as f:
        for sid, _, _, *classes in [line.split(',') for line in f.read().splitlines(keepends=False)]:
            out.extend([f'{c.rpartition("-")[0].strip()},2020,{sid}' for c in classes if len(c.strip()) > 0])
    return out
