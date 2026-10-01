# Programming Exercise 5
## Object-oriented Spatial Modeling with UML

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
| Future Rule | Testing and Validation | N | This will be used to demonstrate the possibility of the code to have extensions or additions in the future. |