WORKOUTS = {'mon': 'upper body #1',
            'tue': 'lower body #1',
            'wed': '30 min cardio',
            'thu': 'upper body #2',
            'fri': 'lower body #2'}


def print_workout_days(workout: str, my_workouts: dict = WORKOUTS) -> None:
    """Print the days (comma separated and title cased) of WORKOUTS
       that (partially) match the workout string passed in. If no
       workout matches, print 'No matching workout'
    """
    days = [day.title() for day, wo in WORKOUTS.items()
            if workout.lower() in wo.lower()]
    print(', '.join(days) if days else 'No matching workout')
