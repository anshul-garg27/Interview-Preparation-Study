# Association

## What Is It?
A **"uses-a"** relationship between two independent classes. Neither class
owns the other. Both have independent lifecycles.

## Types
```
Unidirectional:  Student ──────> Course    (Student knows Course)
Bidirectional:   Doctor <──────> Patient   (both know each other)
```

## Association vs Aggregation vs Composition
| Relationship | Strength | Lifecycle | Example |
|-------------|----------|-----------|---------|
| Association | Weakest | Independent | Student-Course |
| Aggregation | Medium | Independent | Department-Employee |
| Composition | Strongest | Coupled | Car-Engine |

## Multiplicity
- **1:1** - Person has one Passport
- **1:N** - Teacher has many Students
- **M:N** - Students enroll in many Courses, Courses have many Students

## Bidirectional Pitfalls
- Must maintain **both sides** of the relationship
- Risk of **circular references** (Python handles via garbage collector)
- Consider using a **mediator** for complex relationships

## Interview Tip
> "Association = two objects that interact but live independently. Think
> Teacher-Student. Aggregation adds weak ownership. Composition adds strong
> ownership with coupled lifecycles."

## Files in This Folder
| File | Concept |
|------|---------|
| `association_types.py` | Unidirectional (Student-Course), Bidirectional (Doctor-Patient) |
