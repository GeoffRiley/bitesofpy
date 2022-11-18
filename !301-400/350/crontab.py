from dataclasses import dataclass, field
from datetime import datetime

LIMITS = {
    'minutes': (0, 59),
    'hours': (0, 23),
    'days': (1, 31),
    'months': (1, 12)
}


def _parse_part_(element: str, lim_lo: int, lim_hi: int):
    """Parse a crontab element

    Parameters:
        element: a string containing a single crontab element
        lim_lo: an integer representing the lowest acceptable value
        lim_hi: an integer representing the highest acceptable value

    Returns:
         an array of integers that satisfy the given element description

    The element may contain wildcard and multiple event information of a single kind following these rules:
        * : wildcard. May appear on its own indicating any value, eg minutes would mean it represented any of 0–59.
            Alternatively it may be combined with a repetition '/' and an integer value representing the frequency,
            eg */2 in the hours parameter would represent only even (0, 2, 4, 6…) hours.
        / : repetition. See '*' above. May only be used with wildcards.
        , : value list separator. Multiple values may be given separated by a comma alone: no spaces.
        - : value range. A value inclusive range of values may be represented, eg 4-8 would represent 4,5,6,7 and 8.

    No negative values are allowed.
    """
    result_array = []
    if '*' in element:
        # We have a wildcard
        # verify that it is the first character
        _process_wildcard(element, lim_hi, lim_lo, result_array)
    elif ',' in element:
        # possibly multiple value list
        _process_value_list(element, lim_hi, lim_lo, result_array)
    elif '-' in element:
        # a value range element
        _process_value_range(element, result_array)
    else:
        # Just a plain value
        _process_plain_value(element, lim_hi, lim_lo, result_array)
    return set(result_array)


def _process_plain_value(element, lim_hi, lim_lo, result_array):
    p = int(element)
    if not (lim_lo <= p <= lim_hi):
        raise ValueError(f'Value must be in range {lim_lo} to {lim_hi}')
    result_array.append(p)


def _process_value_range(element, result_array):
    parts = element.split('-')
    if len(parts) != 2:
        raise ValueError('Value range element can only contain two parts')
    start, stop = map(int, parts)
    if stop < start:
        raise ValueError('Value range elements must be an increasing range')
    result_array.extend(range(start, stop + 1))


def _process_value_list(element, lim_hi, lim_lo, result_array):
    if not set(element).issubset('1234567890,'):
        raise ValueError('Value list may only contain positive values and commas')
    parts = list(map(int, element.split(',')))
    if min(parts) < lim_lo or max(parts) > lim_hi:
        raise ValueError(f'Value in list, {p}, out of limits {lim_lo} to {lim_hi}')
    result_array.extend(parts)


def _process_wildcard(element, lim_hi, lim_lo, result_array):
    if element[0] != '*':
        raise ValueError('Wildcard elements must BEGIN with the star')
    step = 1
    if '/' in element:
        # the repetition operator can only appear in a wildcard element
        if element[1] != '/':
            raise ValueError('Repetition elements must begin with "*/"')
        step = int(element[2:])
        if step < 1 or step > lim_hi:
            raise ValueError(f'Repetition step must be greater than 1 and less than {lim_hi}')
    result_array.extend([x for x in range(0, lim_hi + 1, step) if x >= lim_lo])


def _find_next(valid_lst: set, current: int):
    if len(valid_lst) == 1:
        # the is only the single value here
        return list(valid_lst)[0]
    new_set = [x for x in valid_lst if x > current]
    if len(new_set):
        # the new value is the minimum of this new set
        return min(new_set)
    # otherwise it's the minimum of the lot
    return min(valid_lst)


@dataclass
class CrontabScheduler:
    """A scheduler based on cron expressions.

    The scheduler can be used to get the next scheduled datetime based on a reference datetime now.

    Attributes:
        expr (str): A valid cron expression (with four parts only, we dont use the fifth part in this bite).
        now (datetime): The reference datetime for which the next datetime should be determined.
        ... hopefully more attributes added by you!

    Raises:
        ValueError: Whenever a value for a cron expression part is not valid.
    """

    expr: str
    now: datetime
    minutes: set = field(init=False)
    hours: set = field(init=False)
    days: set = field(init=False)
    months: set = field(init=False)

    def __post_init__(self):
        parts = self.expr.split()
        if len(parts) != 4:
            raise ValueError(f'Expected 4 cron parts and got {len(parts)}')
        for (name, (lo, hi)), part in zip(LIMITS.items(), parts):
            tmp = _parse_part_(part, lo, hi)
            setattr(self, name, tmp)

    def __iter__(self):
        return self

    def __next__(self) -> datetime:
        # Right now this returns the input datetime now, so you can run all tests and see how it works.
        # However, you are supposed to implement your own logic here to return the next
        # datetime according to the bite description.
        # A flag to indicate when we've moved on
        time_updated = False
        # First ensure that all parts are valid, anything invalid triggers an automatic forward move
        curr = self.now.month
        if curr not in self.months:
            proposed = _find_next(self.months, curr)
            if proposed < curr:
                self.now = self.now.replace(year=self.now.year + 1)
            self.now = self.now.replace(month=proposed, day=min(self.days), hour=min(self.hours),
                                        minute=min(self.minutes))
            time_updated = True
        else:
            curr = self.now.day
            if curr not in self.days:
                proposed = _find_next(self.days, curr)
                if proposed < curr:
                    self.now = self.now.replace(month=self.now.month + 1)
                self.now = self.now.replace(day=proposed, hour=min(self.hours), minute=min(self.minutes))
                time_updated = True
            else:
                curr = self.now.hour
                if curr not in self.hours:
                    proposed = _find_next(self.hours, curr)
                    if proposed < curr:
                        self.now = self.now.replace(day=_find_next(self.days, self.now.day))
                    self.now = self.now.replace(hour=proposed, minute=min(self.minutes))
                    time_updated = True

        # Advance self.now to satisfy the conditions described by all the various cron elements
        if not time_updated:
            curr = self.now.minute
            proposed = _find_next(self.minutes, curr)
            if proposed > curr:
                time_updated = True
            self.now = self.now.replace(minute=proposed)
        if not time_updated:
            curr = self.now.hour
            proposed = _find_next(self.hours, curr)
            if proposed > curr:
                time_updated = True
            self.now = self.now.replace(hour=proposed)
        if not time_updated:
            curr = self.now.day
            proposed = _find_next(self.days, curr)
            if proposed > curr:
                time_updated = True
            self.now = self.now.replace(day=proposed)
        if not time_updated:
            curr = self.now.month
            proposed = _find_next(self.months, curr)
            if proposed > curr:
                time_updated = True
            self.now = self.now.replace(month=proposed)
        return self.now
