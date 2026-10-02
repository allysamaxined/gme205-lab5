from shapely.geometry import box
from src.assessment import ParcelAssessment
from src.rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule, RuleResult
from src.spatial import Parcel, HazardZone

def test_fixed_scenario_and_polymorphism():
    parcel_1 = Parcel("P-001", box(0, 0, 80, 90), "Residential", 7200)
    parcel_2 = Parcel("P-002", box(120, 0, 190, 80), "Commercial", 5600)
    hazard = HazardZone("HZ-01", box(60, 50, 110, 100), "Flood", "High")

    rules =  [
        MinimumAreaRule(5000),
        AllowedZoneRule({"Residential", "Commercial"}),
        NoHazardOverlapRule(hazard),
    ]

    results_1 = ParcelAssessment(parcel_1, rules).evaluate()
    assessment_2 = ParcelAssessment(parcel_2, rules)
    results_2 = assessment_2.evaluate()

    assert [result.passed for result in results_1] == [True, True, False]
    assert len (results_2) == 3
    assert all(isinstance(result, RuleResult) for result in results_2)
    assert [result.passed for result in results_2] == [True, True, True]
    assert assessment_2.passed() is True