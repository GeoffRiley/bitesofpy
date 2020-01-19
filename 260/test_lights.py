import pytest

from lights import LightsGrid


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Turn on all lights
        (["turn on 0,0 through 9,9"], 100),
        # Turn on all lights
        # Turn off selection of lights
        # Turn on all lights again, intensity should be 100
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "turn on 0,0 through 9,9",
                ],
                100,
        ),
        # Turn on all lights
        # Turn off 50 of the lights, intensity decreases 50
        # Turn on 1/4 the lights again, intensity increases 25
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,9",
                    "turn on 0,0 through 4,4",
                ],
                75,
        ),
        # Turn on all lights 3 times
        # Intensity should not go above 100
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn on 0,0 through 9,9",
                    "turn on 0,0 through 9,9",
                ],
                100,
        ),
    ],
)
def test_turn_on_lights(arg, expected):
    lights = LightsGrid(10, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Turn off all lights even though they are not on
        (["turn off 0,0 through 9,9"], 0),
        # Turn on all lights
        # Turn off all lights
        (["turn on 0,0 through 9,9", "turn off 0,0 through 9,9"], 0),
        # Turn on all lights
        # Turn up all lights again intensity should increase 100
        # Turn off 1/4 of all lights, intensity should decrease 50
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn up 1 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                ],
                150,
        ),
        # Turn on all lights
        # Turn up all lights again intensity should increase 100
        # Turn off 1/4 of all lights, decrease 50
        # Turn off an over lapping sect10n, decrease 50
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn up 1 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "turn off 3,3 through 5,5",
                ],
                140,
        ),
    ],
)
def test_turn_off_lights(arg, expected):
    lights = LightsGrid(10, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Toggle all lights
        (["toggle 0,0 through 9,9"], 300),
        # Turn on all lights
        # Toggle all light
        (["turn on 0,0 through 9,9", "toggle 0,0 through 9,9"], 0),
        # Turn on all lights in grid
        # Turn off some lights
        # Toggle some off lights on
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "toggle 3,3 through 6,6",
                ],
                75,
        ),
    ],
)
def test_toggle_lights(arg, expected):
    lights = LightsGrid(10, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Turn on all lights
        # Turn up all light 1
        (["turn on 0,0 through 9,9", "turn up 1 0,0 through 9,9"], 200),
        # Turn on all lights
        # Turn off some lights
        # turn up some lights 3
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "turn up 3 0,0 through 4,9",
                ],
                225,
        ),
        # Turn on all lights
        # Turn off some lights
        # turn up all lights 5
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "turn up 5 0,0 through 9,9",
                ],
                500,
        ),
    ],
)
def test_turn_up_lights(arg, expected):
    lights = LightsGrid(10, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Turn on all lights
        # Turn down 1 all light
        (["turn on 0,0 through 9,9", "turn down 1 0,0 through 9,9"], 0),
        # Turn on all lights
        # Turn off some lights
        # turn up some lights 3
        # Turn down 2 some lights
        (
                [
                    "turn on 0,0 through 9,9",
                    "turn off 0,0 through 4,4",
                    "turn up 3 0,0 through 4,9",
                    "turn down 2 0,5 through 4,9",
                ],
                175,
        ),
        # Turn on all lights
        # turn down 2 all lights
        (["turn on 0,0 through 9,9", "turn down 2 0,0 through 9,9"], 0),
    ],
)
def test_turn_down_lights(arg, expected):
    lights = LightsGrid(10, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected


@pytest.mark.parametrize(
    "arg, expected",
    [
        # Create grid of length 5 - intensity 0
        # Turn on 1,1 through 3,3 - intensity 9
        # Turn off 2,2 through 2,2 - intensity 8
        # Turn up 3 0,2 through 4,2 - intensity 23
        # Toggle 2,0 through 2,4 - intensity 24
        # Turn down 2 2,2 through 3,4 - intensity 19
        (
                [
                    "turn on 1,1 through 3,3",
                    "turn off 2,2 through 2,2",
                    "turn up 3 0,2 through 4,2",
                    "toggle 2,0 through 2,4",
                    "turn down 2 2,2 through 3,4",
                ],
                19,
        )
    ],
)
def test_example_with_bite(arg, expected):
    lights = LightsGrid(5, arg)
    lights.follow_instructions()
    assert lights.lights_intensity == expected
