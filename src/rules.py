# RuleResult, AssessmentRule, and Rule Classes

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class RuleResult:
    rule_name: str
    passed: bool
    message: str

class AssessmentRule(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def evaluate(self, parcel) -> RuleResult:
        pass

class MinimumAreaRule(AssessmentRule):
    def __init__(self, min_area):
        super().__init__("Minimum parcel area")
        self._min_area = float(min_area)

    def evaluate(self, parcel):
        passed = parcel.area_sqm >= self._min_area
        message = (
            f"{parcel.area_sqm:.0f} m² >= {self._min_area:.0f} m²"
            if passed
            else f"{parcel.area_sqm:.0f} m² < {self._min_area:.0f} m²"
        )
        return RuleResult(self.name, passed, message)

class AllowedZoneRule(AssessmentRule):
    def __init__(self, allowed_zones):
        super().__init__("Allowed zone")
        self._allowed_zones = set(allowed_zones)

    def evaluate(self, parcel):
        passed = parcel.zone in self._allowed_zones
        message = (
            f"{parcel.zone} is allowed"
            if passed
            else f"{parcel.zone} is not allowed"
        )
        return RuleResult(self.name, passed, message)

class NoHazardOverlapRule(AssessmentRule):
    def __init__(self, hazard_zone):
        super().__init__("No hazard overlap")
        self._hazard_zone = hazard_zone

    def evaluate(self, parcel):
        passed = not parcel.intersects(self._hazard_zone)
        message = (
            "Parcel does not intersect with the hazard zone."
            if passed
            else "Parcel intersects with the hazard zone."
        )
        return RuleResult(self.name, passed, message)

class RoadAccessRule(AssessmentRule):
    def __init__(self, road, max_distance):
        super().__init__("Road access")
        self._road = road
        self._max_distance = float(max_distance)

    def evaluate(self, parcel):
        distance = parcel.geometry.distance(self._road.geometry)
        passed = distance <= self._max_distance
        message = (
            f"{distance:.0f} <= {self._max_distance:.0f}"
            if passed
            else f"{distance:.0f} > {self._max_distance:.0f}"
            )

        return RuleResult(self.name, passed, message)