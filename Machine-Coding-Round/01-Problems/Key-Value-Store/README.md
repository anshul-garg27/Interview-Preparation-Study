# In-Memory Key-Value Store

## Problem Statement

Design and implement an **In-Memory Key-Value Store** with support for transactions,
TTL (Time-to-Live) for keys, and point-in-time snapshots. The store should support
basic GET/SET/DELETE operations plus advanced features like BEGIN/COMMIT/ROLLBACK
transactions.

**Time Limit**: 90 minutes

---

## Requirements

### Functional Requirements

1. **Basic Operations**
   - `SET key value` - Set a key to a value (create or update)
   - `GET key` - Get the value for a key (returns NULL if not found)
   - `DELETE key` - Delete a key
   - `EXISTS key` - Check if a key exists (returns TRUE/FALSE)
   - `KEYS` - List all keys in the store

2. **Transaction Support**
   - `BEGIN` - Start a new transaction (can be nested)
   - `COMMIT` - Commit the current transaction (apply all changes)
   - `ROLLBACK` - Rollback the current transaction (discard all changes)
   - Nested transactions: BEGIN within BEGIN creates a nested transaction
   - ROLLBACK only rolls back the innermost transaction
   - COMMIT applies all pending transactions

3. **TTL (Time-to-Live)**
   - `SET key value TTL seconds` - Set a key with expiration time
   - Keys automatically expire after TTL seconds
   - Expired keys are not returned by GET and not counted by EXISTS
   - `TTL key` - Show remaining TTL for a key (-1 if no TTL, -2 if not found)

4. **Snapshots**
   - `SNAPSHOT` - Take a point-in-time snapshot of the store
   - `RESTORE snapshot_id` - Restore the store to a previous snapshot
   - Snapshots capture all key-value pairs at the moment

5. **Edge Cases**
   - GET on non-existent key returns NULL
   - DELETE on non-existent key shows error
   - ROLLBACK without BEGIN shows error
   - COMMIT without BEGIN shows error

### Non-Functional Requirements
- In-memory storage (dict/HashMap)
- Command-line style interface (parse text commands)
- Clean output showing each operation and result

---

## Sample Input/Output

```
> SET name Alice
OK

> SET age 30
OK

> GET name
Alice

> EXISTS name
TRUE

> GET unknown
NULL

> DELETE name
OK

> GET name
NULL

> BEGIN
OK (Transaction started, depth: 1)

> SET name Bob
OK

> SET city NYC
OK

> GET name
Bob

> ROLLBACK
OK (Transaction rolled back, depth: 0)

> GET name
NULL

> GET city
NULL

> BEGIN
OK (Transaction started, depth: 1)

> SET name Charlie
OK

> BEGIN
OK (Transaction started, depth: 2)

> SET name Diana
OK

> ROLLBACK
OK (Transaction rolled back, depth: 1)

> GET name
Charlie

> COMMIT
OK (Transaction committed)

> GET name
Charlie

> SET temp_key hello TTL 5
OK (expires in 5 seconds)

> TTL temp_key
5

> SNAPSHOT
Snapshot S-001 created (3 keys)

> KEYS
age: 30
name: Charlie
temp_key: hello
```

---

## Class Diagram

```
┌────────────────────┐
│  KeyValueStore      │
│                     │
│ - _data: dict       │
│ - _ttl_mgr          │
│ - _txn_mgr          │
│ - _snapshot_mgr     │
│                     │
│ + get(key)          │
│ + set(key, value)   │
│ + delete(key)       │
│ + exists(key)       │
│ + keys()            │
└─────────┬───────────┘
          │ uses
    ┌─────┴──────┬──────────────┐
    v            v              v
┌──────────┐ ┌──────────┐ ┌──────────┐
│ TxnMgr   │ │ TTLMgr   │ │ SnapMgr  │
│          │ │          │ │          │
│ +begin() │ │ +set_ttl│ │ +take()  │
│ +commit()│ │ +check() │ │ +restore│
│ +rollback│ │ +get_ttl│ │ +list()  │
└──────────┘ └──────────┘ └──────────┘

┌──────────────────┐
│ CommandParser     │
│                   │
│ + parse(line)     │
│ + execute(cmd)    │
└──────────────────┘
```

---

## File Structure

```
code/
├── key_value_store.py   # Main store with GET, SET, DELETE, EXISTS
├── transaction.py       # BEGIN, COMMIT, ROLLBACK support
├── ttl_manager.py       # Time-to-live management
├── snapshot.py          # Point-in-time snapshots
├── command_parser.py    # Parse and execute text commands
└── demo.py              # Full working demo
```

---

## Evaluation Criteria

| Criteria | Points | What They Look For |
|----------|--------|--------------------|
| Executable | 30 | demo.py runs, GET/SET/DELETE work |
| Modularity | 25 | Store, TTL, Transactions separated |
| Extensibility | 15 | Easy to add new commands |
| Edge Cases | 15 | Missing keys, no transaction, expired TTL |
| Patterns | 10 | Command pattern for operations, clean parser |
| Bonus | 5 | Nested transactions, snapshots |

---

## Hints

1. **Transaction stack**: Use a list of dicts as a transaction stack. Each BEGIN pushes
   a new dict. SET/DELETE modify the top dict. COMMIT merges down. ROLLBACK pops.
2. **TTL**: Store expiry timestamps. On every GET, check if the key has expired.
3. **Snapshots**: Deep copy the data dict at snapshot time.
4. **Command parsing**: Split on whitespace, first token is the command.

---

## Extension Ideas (If You Finish Early)

- INCR/DECR for numeric values
- EXPIRE command to set TTL on existing key
- PERSIST command to remove TTL from a key
- WATCH key (get notified on change)
- MULTI/EXEC (batch commands)
