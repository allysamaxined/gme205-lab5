# Programming Exercise 5
## Object-oriented Spatial Modeling with UML

### Introduction to the Programming Exercise
This programming exercise focuses on modelling a small parcel-development assessment system before actual coding. Here, I used UML to make classes, responsibilities, and relationships visible, and then converted that design to Python. At the end or after finishing this exercise, I was able to design a project that embodies the core idea object-oriented analysis and design, which was separating understanding from implementation. 

### Materials/Requirements
1. Python
2. VS Code
3. Git/GitHub
4. Shapely
5. JSON Output
6. pytest
7. UML tool (draw.io)

### Python Libraries Used
1. Shapely
2. json
3. pytest
4. abc
5. dataclasses

### Project Structure
The structure of the project is as follows:
```
gme205-lab5/
    .venv/
    diagrams/
        lab5_uml.png
    output/
        lab5_report.json
    src/
        assessment.py
        demo.py
        rules.py
        run_lab5.py
        spatial.py
    tests
        test_assessment.py
        test_rules.py
        test_spatial.py
    .gitignore
    README.md
    requirements.txt
```

### Environment Setup
1. Create the root directory.
2. Open VS Code > root folder > create the virtual environment.
```
python -m venv .venv
```
3. Activate the venv using:
```
.\.venv\Scripts\activate
```
4. Select Python Interpreter and install required dependencies.
```
pip install --upgrade pip
pip install shapely pytest
pip install -r requirements.txt
pip freeze > requirements.txt
```
5. (.venv) Must be activated, commands must be executed in the root directory.

### Problem Statement
A local planning team wants to build a program that will help them assess parcels based on their development rules and criteria. They want to build a program where a parcel stands as a class of its own, with identity, geometry, zoning, and area in square meters.

To assess these parcels, they need to run it under three rules:
1. It has to have a minimum area;
2. It has to be within the allowed zones; and
3. If a parcel intersects a hazard zone, it should be rejected.

Every rule must return either a confirmation or rejection with the rule name, and an explanation about what has been assessed. Should a parcel be assessed, it will be ran through every rule and will produce a report. 

The program must be future-rule-proof; it should let the planning team add more rules should they be needing it in the future, without having to rewrite the entire thing.

### Candidate-Class Table
| Phrase from the Problem Statement | Initial Interpretation | Keep as class? (Y/N) | Reason |
| --------------------------------- | ---------------------- | -------------------- | ------ |
| Local Planning Team | Actor/Stakeholder | N | Local planning team uses the system, but not part of this small domain model. |
| Parcel | Domain Entity | Y | Owns an identity, state, and geometry behavior. |
| Zoning Classification | Parcel State | N | A value that's carried by parcel. (Allowed set of zones.) |
| Geometry | Attribute/Value | N | Information belonging to the object. |
| Parcel Area | Attribute/Value | N | Information belonging to the object. |
| Assessment Rule | Behavioral Abstraction | Y | This will determine the contract or rule that is common among all variants. It should also allow future rules to be added without having to rewrite. |
| Minimum Area Rule | Specialized Rule | Y | Owns a threshold and one evaluation behavior. |
| Allowed Set of Zones | Rule Configuration | N | Collection of allowed zones, not necessarily an object of its own. |
| Allowed Zone Rule | Specialized Rule | Y | Owns the configuration and assesses if a parcel's zone rule is acceptable. |
| Hazard Zone | Domain Entity | Y | Owns an identity, geometry, type, and severity. |
| No Hazard Overlap Rule | Specialized Rule | Y | Evaluates if parcels overlap with a hazard-identified area and returns a RuleResult. |
| Rule Result | Value Object | Y | This will provide one consistent result shape from all the rules. |
| Parcel Assessment | Coordinator | Y | This will be used to assess the parcel. |
| Report | Output Representation | N | A JSON report will be sufficient for this programming exercise, lacks enough responsibility to be a class. |
| Future Rule | Extension Possibility | N | This will be used to demonstrate the possibility of the code to have extensions or additions in the future. |

### Extension without coordinator rewrite
This section shows and compares the original rules and new rules list, as well as the unchanged ParcelAssessment.evaluate() method.

The original rules list goes as follows:
```
rules = [
    MinimumAreaRule(5000),
    AllowedZoneRule({"Residential", "Commercial"}),
    NoHazardOverlapRule(hazard),
]
```
The new rules list becomes:
```
rules = [
    MinimumAreaRule(5000),
    AllowedZoneRule({"Residential", "Commercial"}),
    NoHazardOverlapRule(hazard),
    RoadAccessRule(road, 30),
]
```
The `ParcelAssessment.evaluate()` remains as is, unchanged:
```
def evaluate(self):
    results = []
    for rule in self._rules:
        result = rule.evaluate(self._parcel)
        results.append(result)
    return results
```
In this design, no coordinator rewrite had to be done. RoadAccessRule, the new rule, followed the same `AssessmentRule` contract as the original. It also implements `evaluate(parcel)` and returns a `RuleResult`. From here, `ParcelAssessment` can process it under the same loop.

Unlike adding `elif` branches, this does not check each rule's concrete type. Future rules like RoadAccessRule was able to participate by inheriting from `AssessmentRule`, and being added to the list of rules. If an `elif` approach was used, every new rule would require modifying the coordinator.

### Reflection Questions and Answers
**1. OOAD: What changed in your thinking when you modeled the problem before writing the class implementations?**
Modeling the problem before writing the class implementation changed my way of thinking, in a way that it zooms in and focuses on one specific thing first, before proceeding to the other. It's in a way that makes me feel like I'm investigating something very closely, providing it with specific information and identity, before moving forward to doing anything else. It made me fix how I look at objects, in general. In the past, I used to think that I always have to start writing the code and fix it later on. With the past laboratories and especially this one, it helped me understand that there's a reason why we have to understand and design first, before we code. It helped me understand what each other knows, what should be included in or under them, and to process one concept at a time. What changed the game for me was the UML tool. It helped a lot with visualizing how the entire project looks like, making it easier to implement and write.```

**2. Candidate Classes: Name one noun from the problem statement that you intentionally did not make into a class. Why?**
The noun from the problem statement that I intentionally left and did not turn into class was the *report*. This is because it only represents the assessment results using a .JSON format. It does not have enough responsibility and/or meaningful behavior. If there will be a need to use it for filtering or formatting purposes, it should be transformed into class.

**3. Encapsulation: Which Parcel state is protected by its interface, and what invalid state does the constructor prevent?**
The Parcel state that's protected by its interface is *area_sqm*. It is under a read-only property and its constructor prevents a parcel from being created with zero or negative value, and raises a ValueError. Here's a snippet of that part of the script.
```
class Parcel:
    def __init__(self, parcel_id, geometry, zone, area_sqm):
        if not parcel_id:
            raise ValueError("parcel_id is required")
        if not zone:
            raise ValueError("zone is required")
        if float(area_sqm) <= 0:
            raise ValueError("area_sqm must be positive")

        self._parcel_id = str(parcel_id)
        self._geometry = geometry
        self._zone = str(zone)
        self._area_sqm = float(area_sqm)

    @property
    def parcel_id(self):
        return self._parcel_id

    @property
    def zone(self):
        return self._zone

    @property
    def area_sqm(self):
        return self._area_sqm

    @property
    def geometry(self):
        return self._geometry

    def intersects(self, other):
        return self._geometry.intersects(other.geometry)
```

**4. Abstraction: What does AssessmentRule promise without knowing the details of a specific rule?**
AssessmentRule keeps the abstraction and the property of the rules even without knowing the full details about each one. It promises to implement `evaluate(parcel)` and return a `RuleResult` that contains the name of the rule, the decision, and the message. It does not hinder or define how specifically a rule evaluates a parcel, so new rules can be added while still following the same interface.

**5. Inheritance: What code or contract is shared by the concrete rule subclasses?**
All three (3), now four (4) rule subclasses inherit from AssessmentRule. All four share its name and contract, in order to run or implement `evaluate(parcel)` and return a `RuleResult`, while allowing each subclass to return its own evaluation.

**6. Polymorphism: Why can ParcelAssessment call evaluate(parcel) without knowing which concrete rule object it received?**
Based on how the ParcelAssessment is designed in `assessment.py`, it can call `evaluate(parcel)` even without knowing which concrete rule object it receives because each concrete rule follows the same interface. it passes the parcel to each of these rules, and lets it check its own condition and evaluate. Afterward, it will return a `RuleResult`.

**7. Composition: Why is ParcelAssessment better modeled as having a Parcel and rules rather than inheriting from them?**
It is better modeled this way, having one Parcel and a collection of rules, since it coordinates those objects to perform an assessment. In itself, it's not a parcel or a rule, so making it inherit from them won't represent the relationship correctly. This way, as well, each class is focused on its own responsibility.

**8. Extension: What did you add for the new rule: and what existing code did you not need to change?**
I added `RoadAccessRule` as the new rule. Specifically, I designed it to contain a way to assess a nearby and distant parcel, to check whether a parcel is within the allowed distance of a road. The existing code that I did not need to change was `ParcelAssessment.evaluate()`.

**9. UML-to-code Consistency: Give one example where the final diagram helped you detect or correct a code-structure problem.**
When I was designing the `NoHazardOverlapRule`, I specifically relied on the final diagram to design it properly. It helped me understand what needs to be included in the class, to make `HazardZone` a separate class, and know what to include in it, such as its ID and geometry. 