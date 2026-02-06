# File System - Low Level Design

## Problem Statement
Design an in-memory file system that supports files and directories, CRUD operations, searching, permissions, tree display, and size calculations. This is a classic showcase of the **Composite pattern**.

---

## Functional Requirements
1. **Create** files and directories
2. **Delete** files and directories (recursive)
3. **Move/Rename** files and directories
4. **Search** by name, extension, or size
5. **Permissions** - Read, Write, Execute per file/directory
6. **Tree Display** - Visual directory tree like `tree` command
7. **Size Calculation** - File size and recursive directory size
8. **Path Navigation** - Absolute path resolution

## Non-Functional Requirements
- Efficient tree traversal for large hierarchies
- Thread-safe for concurrent access
- Support deep nesting without stack overflow

---

## Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Composite** | File/Directory hierarchy | Treat files and directories uniformly |
| **Iterator** | Tree traversal (DFS/BFS) | Traverse tree without exposing internals |
| **Visitor** | Operations (size calc, search, display) | Add new operations without modifying nodes |

### Composite Pattern (Core)
Both `File` and `Directory` implement the `FileSystemNode` interface. A Directory contains a list of `FileSystemNode` children, which can be either Files or other Directories. This allows recursive operations (size, delete, display) to work uniformly.

### Iterator Pattern
Custom iterators for depth-first and breadth-first traversal of the file tree. Clients iterate without knowing the tree structure.

### Visitor Pattern
Operations like size calculation, search, and tree display are implemented as visitors. This lets us add new operations (e.g., "find duplicates", "compress") without modifying the File/Directory classes.

---

## Class Diagram

```mermaid
classDiagram
    class FileSystemNode {
        <<abstract>>
        -String name
        -Permission permissions
        -datetime created_at
        -datetime modified_at
        -FileSystemNode parent
        +get_name() String
        +get_path() String
        +get_size() int
        +is_directory() bool
        +accept(visitor) *
    }

    class File {
        -int size
        -String extension
        -String content
        +get_size() int
        +is_directory() bool
        +accept(visitor)
    }

    class Directory {
        -Map~String, FileSystemNode~ children
        +add(node)
        +remove(name)
        +get_child(name) FileSystemNode
        +list_children() List~FileSystemNode~
        +get_size() int
        +is_directory() bool
        +accept(visitor)
    }

    class Permission {
        -bool read
        -bool write
        -bool execute
        +can_read() bool
        +can_write() bool
        +can_execute() bool
        +to_string() String
    }

    class FileSystemVisitor {
        <<interface>>
        +visit_file(file)
        +visit_directory(directory)
    }

    class SizeCalculatorVisitor {
        -int total_size
        +visit_file(file)
        +visit_directory(directory)
        +get_total_size() int
    }

    class SearchVisitor {
        -String query
        -List results
        +visit_file(file)
        +visit_directory(directory)
        +get_results() List
    }

    class TreeDisplayVisitor {
        -int depth
        +visit_file(file)
        +visit_directory(directory)
    }

    class FileSystem {
        -Directory root
        +create_file(path, name, size)
        +create_directory(path, name)
        +delete(path)
        +move(src, dest)
        +search(query) List
        +display_tree()
        +get_size(path) int
        -resolve_path(path) FileSystemNode
    }

    FileSystemNode <|-- File
    FileSystemNode <|-- Directory
    FileSystemNode --> Permission
    Directory o-- FileSystemNode : children
    FileSystemVisitor <|.. SizeCalculatorVisitor
    FileSystemVisitor <|.. SearchVisitor
    FileSystemVisitor <|.. TreeDisplayVisitor
    FileSystem --> Directory : root
    FileSystem ..> FileSystemVisitor
```

---

## Sequence Diagram - Creating a File

```mermaid
sequenceDiagram
    participant C as Client
    participant FS as FileSystem
    participant D as Directory
    participant F as File

    C->>FS: create_file("/home/docs", "report.txt", 1024)
    FS->>FS: resolve_path("/home/docs")
    FS->>D: get_child("home")
    D-->>FS: home_dir
    FS->>D: get_child("docs") on home_dir
    D-->>FS: docs_dir
    FS->>F: new File("report.txt", 1024)
    FS->>D: add(file) on docs_dir
    D->>D: check permissions (write)
    D->>D: check name collision
    D-->>FS: success
    FS-->>C: File created
```

## Sequence Diagram - Recursive Size Calculation

```mermaid
sequenceDiagram
    participant C as Client
    participant FS as FileSystem
    participant V as SizeCalculatorVisitor
    participant D as Directory
    participant F1 as File1
    participant F2 as File2
    participant SD as SubDirectory
    participant F3 as File3

    C->>FS: get_size("/home")
    FS->>V: new SizeCalculatorVisitor()
    FS->>D: accept(visitor) on /home
    D->>V: visit_directory(self)
    V->>F1: accept(visitor)
    F1->>V: visit_file(self) [size=100]
    V->>F2: accept(visitor)
    F2->>V: visit_file(self) [size=200]
    V->>SD: accept(visitor)
    SD->>V: visit_directory(self)
    V->>F3: accept(visitor)
    F3->>V: visit_file(self) [size=300]
    V-->>C: total_size = 600
```

---

## Edge Cases
1. **Name conflicts** - Cannot create two children with same name in a directory
2. **Delete non-empty directory** - Recursive delete
3. **Move into itself** - Cannot move a directory into its own subtree (cycle)
4. **Path resolution** - Handle `/`, `..`, trailing slashes
5. **Root deletion** - Cannot delete the root directory
6. **Permission denied** - Check write permission before modifications
7. **File vs directory operations** - Cannot add children to a file
8. **Very deep nesting** - Iterative traversal preferred over recursive

## Extensions
- Symbolic links (soft links)
- File content storage and retrieval
- File versioning / history
- Disk space quotas
- File locking for concurrent access
- Compression support
- Wildcard pattern matching (glob)

---

## Interview Tips

1. **Lead with Composite pattern** - This IS the pattern this question tests
2. **Draw the tree structure** - Show how Directory contains FileSystemNode children
3. **Visitor is a bonus** - Not all interviewers expect it, but it demonstrates design maturity
4. **Discuss recursion vs iteration** - Show awareness of stack overflow risk
5. **Permission model** - Keep it simple (rwx booleans), don't over-engineer
6. **Common follow-up**: "How would you implement `find`?" - Use the Visitor or Iterator
7. **Common follow-up**: "Add symbolic links" - Discuss cycle detection
