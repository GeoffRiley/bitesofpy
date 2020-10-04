import re
from datetime import datetime
from typing import List


def get_srt_section_ids(text: str) -> List[int]:
    """Parse a caption (srt) text passed in and return a
       list of section numbers ordered descending by
       highest speech speed
       (= ratio of "time past:characters spoken")

       e.g. this section:

       1
       00:00:00,000 --> 00:00:01,000
       let's code

       (10 chars in 1 second)

       has a higher ratio then:

       2
       00:00:00,000 --> 00:00:03,000
       code

       (4 chars in 3 seconds)

       You can ignore milliseconds for this exercise.
    """
    time_re = re.compile(r'(?P<start>\d+:\d+:\d+),\d+\s-->\s(?P<end>\d+:\d+:\d+),\d+')

    lines = text.splitlines(keepends=False)
    parts = dict()
    for sec, tim, speech in zip(lines, lines[1:], lines[2:]):
        if not sec.isdecimal():
            continue
        tm = time_re.match(tim)
        if not tm:
            continue
        start_time = get_timestamp(tm, 'start')
        end_time = get_timestamp(tm, 'end')
        parts[int(sec)] = len(speech.split()) / (end_time - start_time).total_seconds()
    return [n for n, _ in sorted(parts.items(), key=lambda x: x[1], reverse=True)]


def get_timestamp(tm, time_str):
    return datetime.strptime(tm.group(time_str), '%H:%M:%S')
