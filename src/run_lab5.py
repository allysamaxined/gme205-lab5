from shapely.geometry import box, LineString
from rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule, RoadAccessRule
from spatial import Parcel, HazardZone, Road
from assessment import ParcelAssessment
import json

def main():


    parcel_a = Parcel(
        "P-001",
        box(0, 0, 80, 90),
        "Residential",
        7200,
    )

    parcel_b = Parcel(
        "P-002",
        box(120, 0, 190, 80),
        "Commercial",
        5600,
    )

    hazard = HazardZone(
        "HZ-01",
        box(60, 50, 110, 100),
        "Flood",
        "High",
    )

    road = Road (
        "R-01",
        LineString([(0, 0), (100,0)]),
    )

    rules = [
        MinimumAreaRule(5000),
        AllowedZoneRule({"Residential", "Commercial"}),
        NoHazardOverlapRule(hazard),
        RoadAccessRule(road, 30),
    ]

    assessments = [
        (parcel_a, ParcelAssessment(parcel_a, rules)),
        (parcel_b, ParcelAssessment(parcel_b, rules)),
    ]

    report = {
        "scenario": "parcel-development-assessment",
        "parcels": []
    }

    for parcel, assessment in assessments:
        results = assessment.evaluate()

        report["parcels"].append(
            {
                "parcel_id": parcel.parcel_id,
                "passed": assessment.passed(),
                "results": [
                    {
                        "rule_name": result.rule_name,
                        "passed": result.passed,
                        "message": result.message,
                    }
                    for result in results
                ],
            }
        )

    with open("output/lab5_report.json", "w") as f:
        json.dump(report, f, indent=4)


if __name__ == "__main__":
    main()
