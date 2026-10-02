import pytest
from src.spatial import Parcel, HazardZone
from shapely.geometry import box

def test_parcel_rejects_invalid_state():
    geometry = box(0, 0, 50, 50)

    with pytest.raises(ValueError):
        Parcel("", geometry, "Residential", 2500)

    with pytest.raises(ValueError):
        Parcel("P-001", geometry, "", 2500)

    with pytest.raises(ValueError):
        Parcel("P-001", geometry, "Residential", -1000)

def test_parcel_properties_and_intersects():
    geometry = box(0, 0, 50, 50)
    parcel = Parcel("P-001", geometry, "Residential", 2500)
    hazard = HazardZone(
        "HZ-01",
        box(40, 40, 60, 60),
        "Flood",
        "Low",
    )

    assert parcel.parcel_id == "P-001"
    assert parcel.zone == "Residential"
    assert parcel.area_sqm == 2500
    assert parcel.geometry is geometry
    assert parcel.intersects(hazard) is True