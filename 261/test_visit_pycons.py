from visit_pycons import (
    _get_pycons,
    update_pycons_lat_lon,
    create_travel_plan,
    total_travel_distance,
)


def test_update_pycons_lat_lon():
    pycons = _get_pycons()
    update_pycons_lat_lon(pycons)
    for pycon in pycons:
        assert isinstance(pycon.lat, float)
        assert isinstance(pycon.lon, float)


def test_create_travel_plan():
    pycons = _get_pycons()
    update_pycons_lat_lon(pycons)
    travel_plan = create_travel_plan(pycons)
    assert len(travel_plan) == 8
    assert travel_plan[0].origin.name == "PyCon Odessa"
    assert travel_plan[0].destination.name == "PyCon SK"
    assert travel_plan[-1].origin.name == "PyCon DE & PyData Berlin"
    assert travel_plan[-1].destination.name == "PyCon Ireland"


def test_total_travel_distance():
    pycons = _get_pycons()
    update_pycons_lat_lon(pycons)
    travel_plan = create_travel_plan(pycons)
    assert total_travel_distance(travel_plan) == 8444.9
