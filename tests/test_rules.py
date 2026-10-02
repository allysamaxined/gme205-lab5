import pytest
from shapely.geometry import box
from src.rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule, AssessmentRule, RuleResult
from src.spatial import Parcel, HazardZone

def test_assessment_rule_is_abstract():
    with pytest.raises(TypeError):
        AssessmentRule("Test rule")

def test_minimum_area_rule_passes_and_fails():
    rule = MinimumAreaRule(5000)

    passing = Parcel("P-001", box(0, 0, 10, 10), "Residential", 6000)
    failing = Parcel("P-002", box(0, 0, 10, 10), "Residential", 4000)

    assert isinstance(rule.evaluate(passing), RuleResult)
    assert rule.evaluate(passing).passed is True
    assert rule.evaluate(failing).passed is False

def test_allowed_zone_rule_passes_and_fails():
    rule = AllowedZoneRule({"Residential", "Commercial"})

    allowed = Parcel("P-001", box(0, 0, 10, 10), "Residential", 5000)
    disallowed = Parcel("P-002", box(0, 0, 10, 10), "Agricultural", 5000)

    assert rule.evaluate(allowed).passed is True
    assert rule.evaluate(disallowed).passed is False

def test_hazard_rule_passes_and_fails():
    hazard = HazardZone (
        "HZ-01",
        box(40, 40, 60, 60),
        "Flood",
        "High",
    )

    rule = NoHazardOverlapRule(hazard)

    intersecting = Parcel("P-001", box(0, 0, 50, 50), "Residential", 5000)
    separate = Parcel("P-002", box(100, 100, 150, 150), "Residential", 5000)

    assert rule.evaluate(intersecting).passed is False
    assert rule.evaluate(separate).passed is True