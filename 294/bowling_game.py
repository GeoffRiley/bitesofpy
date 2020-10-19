import itertools
from typing import List, Tuple

SCORE = 'X'
SPARE = '/'
GUTTER = '-'
PASS = ' '


def bowl_value(frame_no: int, frame_list: List[Tuple[str, str]], bowl_number: int) -> int:
    """Calculate the score of a single bowl within a frame"""
    score = 0
    if frame_no >= len(frame_list):
        return 0
    score_ball = frame_list[frame_no][bowl_number]
    if score_ball == PASS:
        if bowl_number != 1:
            raise ValueError(f'Missing first bowl in frame #{frame_no}')
    elif score_ball == GUTTER:
        pass
    elif score_ball == SCORE:
        if bowl_number != 0 and frame_no != 9:
            raise ValueError(f'SCORE registered for second bowl in frame #{frame_no}')
        score = 10
    elif score_ball == SPARE:
        if bowl_number != 1:
            raise ValueError(f'SPARE registered for first bowl in frame #{frame_no}')
        # value is 10 minus the score for the first ball!
        score = 10 - bowl_value(frame_no, frame_list, 0)
    else:
        score = int(score_ball)
    return score


def frame_score(frame_no: int, frame_list: List[Tuple[str, str]]) -> int:
    """Calculate the score of a single frame"""
    score_this = frame_list[frame_no]
    score = 0
    # first bowl can be number of pins, a SCORE or a GUTTER
    if score_this[0] == SCORE:
        # score = 10 plus the next two bowl values (not scores!!)
        next_bowl = bowl_value(frame_no + 1, frame_list, 0)
        if next_bowl == 10:  # i.e. it was another strike
            next_bowl += bowl_value(frame_no + 2, frame_list, 0)
        else:
            next_bowl += bowl_value(frame_no + 1, frame_list, 1)
        score = 10 + next_bowl
    else:
        if score_this[0] == GUTTER:
            # nothing for a gutter ball
            pass
        elif score_this[0] in '123456789':
            score = int(score_this[0])
        else:
            raise ValueError(f'What does "{score_this[0]}" mean for a first bowl? Frame #{frame_no}')

        # second bowl can be number of pins, a SPARE or a GUTTER
        if score_this[1] == SPARE:
            # whatever the first bowl was it's made up to 10
            # plus the next bowl value (not score!!)
            score = 10 + bowl_value(frame_no + 1, frame_list, 0)
        elif score_this[1] == GUTTER:
            # nope, still nothing for that gutter shot
            pass
        elif score_this[1] in '123456789':
            score += int(score_this[1])
        else:
            raise ValueError(f'What does "{score_this[1]}" mean for a second bowl? Frame #{frame_no}')

    return score


def calculate_score(frames: str) -> int:
    """Calculates a total 10-pin bowling score from a string of frame data."""
    # divide up the frames into pairs of characters (making sure the last char is grabbed too)
    frame_list = list(itertools.zip_longest(frames[::2], frames[1::2], fillvalue=PASS))
    # Scoring is off pattern when there is a SCORE on the last frame,
    # so a little massaging is needed
    *frame_list, penultimate, ultimate = frame_list
    if len(frame_list) > 8:
        while penultimate[0] == 'X':
            frame_list.append((penultimate[0], PASS))
            penultimate = (penultimate[1], ultimate[0])
            ultimate = (ultimate[1], PASS)
    frame_list.extend([penultimate, ultimate])
    score = 0
    for frame_no in range(10):
        score += frame_score(frame_no, frame_list)
    return score
