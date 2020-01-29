from flux import XYZ, calculate_flux, identify_flux


def test_calculate():
    calc = calculate_flux(XYZ)
    assert isinstance(calc, list)
    assert len(calc) == 11
    assert len(calc[0]) == 5

    *orig, dol, perc = calc[0]
    assert orig == ["Cash", 120000, 115000]
    assert dol == 5000
    assert round(perc, 2) == 0.04


def test_identify():
    flux = identify_flux(calculate_flux(XYZ))
    assert isinstance(flux, list)
    assert len(flux) == 5
    assert [act for act, *_ in flux] == [
        "Accounts Receivable",
        "Inventory",
        "Notes Receivable",
        "Accrued Payroll",
        "Retained Earnings",
    ]
