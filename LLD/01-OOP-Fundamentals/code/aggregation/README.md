# Aggregation

## What Is It?
A **weak "has-a"** relationship where the contained object exists
independently of the container. The container uses it but doesn't own it.

## Aggregation vs Composition
```
Composition (strong):  Car ◆──── Engine      (engine dies with car)
Aggregation (weak):    Dept ◇──── Employee   (employee survives)
```

| Aspect | Composition | Aggregation |
|--------|------------|-------------|
| Created by | Container creates part | Part passed in from outside |
| Lifecycle | Coupled | Independent |
| UML symbol | Filled diamond (◆) | Empty diamond (◇) |
| Delete container | Parts are destroyed | Parts survive |

## Common Examples
- **Department** has **Employees** (employees can change departments)
- **Playlist** has **Songs** (songs exist in multiple playlists)
- **University** has **Professors** (professors outlive university)

## In Code
```python
# Composition: Car creates its own Engine
self._engine = Engine(200)

# Aggregation: Department receives Employee from outside
def add(self, employee: Employee):
    self._members.append(employee)
```

## Interview Tip
> "Aggregation = 'uses' but doesn't own. The key test: if the container is
> deleted, do the parts survive? If yes, it's aggregation."

## Files in This Folder
| File | Concept |
|------|---------|
| `aggregation_example.py` | Department-Employee relationship |
