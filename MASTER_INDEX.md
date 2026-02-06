# Software Engineering & Computer Science - Master Study Index

> Everything a software engineer needs to know. Organized by domain.
> Status: ✅ Done | 🔨 In Progress | 📋 Planned | ❌ Not Started

---

## 1. LOW LEVEL DESIGN (LLD) / Object Oriented Design ✅

```
Status: ✅ COMPLETE (386 files | 299 .py + 87 .md | 2.4MB)
Path:   ./LLD/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 1.1 | OOP Fundamentals | Classes & Objects, Encapsulation, Abstraction, Inheritance, Polymorphism, Composition, Aggregation, Association, Interfaces | ✅ |
| 1.2 | SOLID Principles | SRP, OCP, LSP, ISP, DIP (each with violation + fix code) | ✅ |
| 1.3 | UML Diagrams | Class, Sequence, State, Activity, Use Case Diagrams | ✅ |
| 1.4 | Design Patterns (22 GoF) | Creational (5), Structural (7), Behavioral (10) — each with modular code | ✅ |
| 1.5 | Design Principles | DRY, KISS, YAGNI, GRASP, Law of Demeter, Code Smells | ✅ |
| 1.6 | LLD Problems (23) | Parking Lot, Elevator, LRU Cache, Chess, BookMyShow, Library, Vending Machine, Cab Booking, Snake Ladder, Online Shopping, ATM, Hotel Booking, Social Media, Tic-Tac-Toe, Notification System, Splitwise, File System, Rate Limiter, URL Shortener, Logging Framework, Food Delivery, Stack Overflow, Payment Gateway | ✅ |
| 1.7 | Concurrency Patterns | Thread Safety, Producer-Consumer, Reader-Writer, Deadlocks, Thread Pool | ✅ |
| 1.8 | Architectural Patterns | DI, Repository, Service Layer, DAO, MVC/MVP/MVVM, Clean Architecture, Event-Driven | ✅ |
| 1.9 | Testing Patterns | TDD, Mocking, Test Doubles, Unit Testing | ✅ |
| 1.10 | API Design Patterns | REST, Versioning, Pagination, Rate Limiting, Authentication | ✅ |
| 1.11 | Refactoring Techniques | 10 Code Smells, 10 Refactoring Techniques | ✅ |
| 1.12 | Interview Prep | Mock Interviews, Scoring Rubrics, Cheat Sheets, Quick Revision, Case Studies | ✅ |

---

## 2. HIGH LEVEL DESIGN (HLD) / System Design ❌

```
Status: ❌ NOT STARTED
Path:   ./HLD/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| **Fundamentals** |
| 2.1 | Scalability | Vertical vs Horizontal, Load Balancing, Auto-scaling | ❌ |
| 2.2 | Availability & Reliability | SLAs, Failover, Redundancy, Replication | ❌ |
| 2.3 | Consistency Models | Strong, Eventual, Causal Consistency, CAP Theorem, PACELC | ❌ |
| 2.4 | Networking Basics | TCP/UDP, HTTP/HTTPS, WebSockets, gRPC, REST vs GraphQL | ❌ |
| 2.5 | DNS & CDN | Domain resolution, Content delivery, Edge caching | ❌ |
| **Building Blocks** |
| 2.6 | Load Balancers | L4 vs L7, Algorithms (Round Robin, Least Connections, Consistent Hashing) | ❌ |
| 2.7 | Caching | Redis, Memcached, Cache-aside, Write-through, Write-back, Eviction policies | ❌ |
| 2.8 | Databases | SQL vs NoSQL, Sharding, Replication, Partitioning, Indexing | ❌ |
| 2.9 | Message Queues | Kafka, RabbitMQ, SQS, Pub-Sub, Event Streaming | ❌ |
| 2.10 | Blob Storage | S3, Object Storage, CDN integration | ❌ |
| 2.11 | Search Systems | Elasticsearch, Inverted Index, Full-text Search | ❌ |
| 2.12 | Rate Limiters | Token Bucket, Sliding Window, Fixed Window, Leaky Bucket | ❌ |
| 2.13 | API Gateway | Authentication, Rate Limiting, Routing, Aggregation | ❌ |
| **Advanced Concepts** |
| 2.14 | Microservices | Service Discovery, Circuit Breaker, Saga Pattern, Service Mesh | ❌ |
| 2.15 | Distributed Systems | Consensus (Raft, Paxos), Leader Election, Distributed Locks | ❌ |
| 2.16 | Data Pipelines | ETL, Stream Processing, Batch Processing, Data Lakes | ❌ |
| 2.17 | Monitoring & Observability | Logging, Metrics, Tracing, Prometheus, Grafana, ELK Stack | ❌ |
| 2.18 | Security | OAuth2, JWT, TLS/SSL, CORS, OWASP Top 10 | ❌ |
| **HLD Problems (20+)** |
| 2.19 | URL Shortener | TinyURL / bit.ly design | ❌ |
| 2.20 | Twitter / Social Feed | News feed, Fan-out, Timeline | ❌ |
| 2.21 | WhatsApp / Chat System | Real-time messaging, presence, group chats | ❌ |
| 2.22 | YouTube / Netflix | Video streaming, encoding, recommendation | ❌ |
| 2.23 | Uber / Ride Sharing | Location tracking, matching, surge pricing | ❌ |
| 2.24 | Instagram | Photo sharing, stories, explore feed | ❌ |
| 2.25 | Dropbox / Google Drive | File sync, versioning, sharing | ❌ |
| 2.26 | Amazon / E-Commerce | Catalog, cart, orders, inventory | ❌ |
| 2.27 | Google Search | Web crawling, indexing, ranking | ❌ |
| 2.28 | Notification System | Push, email, SMS at scale | ❌ |
| 2.29 | Payment System | Transactions, idempotency, reconciliation | ❌ |
| 2.30 | Typeahead / Autocomplete | Trie-based, search suggestions | ❌ |
| 2.31 | Rate Limiter (System) | Distributed rate limiting at scale | ❌ |
| 2.32 | Web Crawler | Distributed crawling, politeness, dedup | ❌ |
| 2.33 | Booking System | Concurrency, overbooking, seat allocation | ❌ |
| 2.34 | Distributed Cache | Consistent hashing, replication | ❌ |
| 2.35 | Key-Value Store | Dynamo-style, LSM Trees, SSTable | ❌ |
| 2.36 | Metrics/Logging System | Time-series DB, aggregation | ❌ |
| 2.37 | Ticket Booking | BookMyShow at scale | ❌ |
| 2.38 | Pastebin | Text sharing, expiry, analytics | ❌ |
| **Interview Prep** |
| 2.39 | Back-of-Envelope Calculations | QPS, Storage, Bandwidth estimation | ❌ |
| 2.40 | HLD Interview Framework | Step-by-step approach, time management | ❌ |
| 2.41 | Cheat Sheets & Quick Revision | Building blocks at a glance | ❌ |

---

## 3. DATA STRUCTURES & ALGORITHMS (DSA) ❌

```
Status: ❌ NOT STARTED
Path:   ./DSA/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| **Data Structures** |
| 3.1 | Arrays & Strings | Two Pointers, Sliding Window, Prefix Sum, Kadane's | ❌ |
| 3.2 | Hashing | HashMap, HashSet, Collision Handling, Custom Hash | ❌ |
| 3.3 | Linked Lists | Singly, Doubly, Circular, Reverse, Merge, Cycle Detection | ❌ |
| 3.4 | Stacks & Queues | Monotonic Stack, Deque, Priority Queue, Circular Queue | ❌ |
| 3.5 | Trees | Binary Tree, BST, AVL, Red-Black, B-Tree, Trie | ❌ |
| 3.6 | Heaps | Min-Heap, Max-Heap, Heap Sort, Top-K Problems | ❌ |
| 3.7 | Graphs | Adjacency List/Matrix, BFS, DFS, Topological Sort | ❌ |
| 3.8 | Advanced DS | Segment Tree, Fenwick Tree, Disjoint Set (Union-Find), Skip List | ❌ |
| **Algorithms** |
| 3.9 | Sorting | Bubble, Selection, Insertion, Merge, Quick, Heap, Radix, Counting | ❌ |
| 3.10 | Searching | Binary Search (and all its variations), Linear Search | ❌ |
| 3.11 | Recursion & Backtracking | N-Queens, Sudoku, Permutations, Subsets, Word Search | ❌ |
| 3.12 | Dynamic Programming | 1D, 2D, Knapsack, LCS, LIS, Coin Change, Matrix Chain, Edit Distance | ❌ |
| 3.13 | Greedy Algorithms | Activity Selection, Huffman, Fractional Knapsack, Job Scheduling | ❌ |
| 3.14 | Graph Algorithms | Dijkstra, Bellman-Ford, Floyd-Warshall, Prim's, Kruskal's, Tarjan's | ❌ |
| 3.15 | String Algorithms | KMP, Rabin-Karp, Z-Algorithm, Trie-based | ❌ |
| 3.16 | Bit Manipulation | AND/OR/XOR, Counting Bits, Single Number, Subsets | ❌ |
| 3.17 | Math & Number Theory | GCD, LCM, Prime Sieve, Modular Arithmetic, Power | ❌ |
| **Patterns (Coding Interview)** |
| 3.18 | Two Pointers | Fast/Slow, Left/Right, Same Direction | ❌ |
| 3.19 | Sliding Window | Fixed Size, Variable Size, String Problems | ❌ |
| 3.20 | Binary Search Variations | Search Space, Answer Binary Search, Rotated Array | ❌ |
| 3.21 | BFS/DFS Patterns | Level Order, Island Problems, Path Finding | ❌ |
| 3.22 | DP Patterns | Fibonacci, 0/1 Knapsack, Unbounded Knapsack, LCS, Palindrome | ❌ |
| 3.23 | Merge Intervals | Overlapping Intervals, Insert Interval, Meeting Rooms | ❌ |
| 3.24 | Top-K / Heap Patterns | Kth Largest, Merge K Lists, Median of Stream | ❌ |
| 3.25 | Monotonic Stack | Next Greater Element, Histogram, Trapping Rain Water | ❌ |
| **Practice** |
| 3.26 | LeetCode Top 75 | Curated must-solve problems | ❌ |
| 3.27 | NeetCode 150 | Categorized interview problems | ❌ |
| 3.28 | Striver SDE Sheet | Popular Indian prep sheet | ❌ |
| 3.29 | Company-Specific | Google, Amazon, Meta, Microsoft tagged problems | ❌ |
| 3.30 | Complexity Analysis | Big-O, Time & Space, Amortized Analysis | ❌ |

---

## 4. DATABASE & SQL ❌

```
Status: ❌ NOT STARTED
Path:   ./Database/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 4.1 | SQL Fundamentals | SELECT, JOIN, GROUP BY, HAVING, Subqueries, CTEs | ❌ |
| 4.2 | Advanced SQL | Window Functions (ROW_NUMBER, RANK, LAG, LEAD), Pivot, Recursive | ❌ |
| 4.3 | Database Design | ER Diagrams, Normalization (1NF-3NF-BCNF), Denormalization | ❌ |
| 4.4 | Indexing | B-Tree, Hash Index, Composite, Covering, Partial Index | ❌ |
| 4.5 | Transactions | ACID, Isolation Levels, Locking, MVCC, Deadlocks | ❌ |
| 4.6 | SQL vs NoSQL | Relational vs Document vs Key-Value vs Column vs Graph | ❌ |
| 4.7 | NoSQL Databases | MongoDB, Cassandra, Redis, DynamoDB, Neo4j | ❌ |
| 4.8 | Sharding & Replication | Horizontal/Vertical Sharding, Master-Slave, Master-Master | ❌ |
| 4.9 | Query Optimization | EXPLAIN, Query Plan, N+1 Problem, Connection Pooling | ❌ |
| 4.10 | Database Internals | WAL, LSM Trees, B+ Trees, Page Layout, Buffer Pool | ❌ |
| 4.11 | Interview Questions | Top 50 SQL queries, Schema design problems | ❌ |

---

## 5. OPERATING SYSTEMS (OS) ❌

```
Status: ❌ NOT STARTED
Path:   ./OS/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 5.1 | Process Management | Process vs Thread, PCB, Context Switching, Fork | ❌ |
| 5.2 | CPU Scheduling | FCFS, SJF, Round Robin, Priority, Multilevel Queue | ❌ |
| 5.3 | Process Synchronization | Mutex, Semaphore, Monitor, Critical Section, Deadlock | ❌ |
| 5.4 | Deadlocks | Detection, Prevention, Avoidance, Banker's Algorithm | ❌ |
| 5.5 | Memory Management | Paging, Segmentation, Virtual Memory, Page Replacement (LRU, FIFO, Optimal) | ❌ |
| 5.6 | File Systems | Inodes, FAT, NTFS, ext4, Journaling | ❌ |
| 5.7 | I/O Management | Buffering, Spooling, DMA, Disk Scheduling | ❌ |
| 5.8 | Inter-Process Communication | Pipes, Message Queues, Shared Memory, Sockets | ❌ |
| 5.9 | Linux Internals | System Calls, Kernel, Shell Commands, Permissions | ❌ |
| 5.10 | Interview Questions | Top 50 OS questions | ❌ |

---

## 6. COMPUTER NETWORKS ❌

```
Status: ❌ NOT STARTED
Path:   ./Networks/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 6.1 | OSI & TCP/IP Models | 7 Layers, Protocols at each layer | ❌ |
| 6.2 | Application Layer | HTTP/HTTPS, FTP, SMTP, DNS, DHCP, WebSockets | ❌ |
| 6.3 | Transport Layer | TCP vs UDP, 3-Way Handshake, Flow Control, Congestion Control | ❌ |
| 6.4 | Network Layer | IP Addressing, Subnetting, CIDR, Routing (OSPF, BGP) | ❌ |
| 6.5 | Data Link & Physical | MAC, ARP, Ethernet, Wi-Fi, Switches vs Routers | ❌ |
| 6.6 | Network Security | TLS/SSL, Firewalls, VPN, HTTPS, Certificate Authority | ❌ |
| 6.7 | REST vs gRPC vs GraphQL | Comparison, when to use which | ❌ |
| 6.8 | Interview Questions | Top 50 Networking questions | ❌ |

---

## 7. PROGRAMMING LANGUAGES ❌

```
Status: ❌ NOT STARTED
Path:   ./Languages/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 7.1 | Java Deep Dive | JVM, GC, Collections, Streams, Multithreading, Spring Boot | ❌ |
| 7.2 | Python Deep Dive | GIL, Decorators, Generators, asyncio, Magic Methods, Metaclasses | ❌ |
| 7.3 | JavaScript/TypeScript | Event Loop, Closures, Promises, async/await, Prototypes | ❌ |
| 7.4 | Go (Golang) | Goroutines, Channels, Interfaces, Error Handling | ❌ |
| 7.5 | C++ Essentials | STL, Pointers, Memory Management, Smart Pointers, Templates | ❌ |
| 7.6 | Language Comparison | Java vs Python vs Go vs C++ (when to use which) | ❌ |

---

## 8. WEB DEVELOPMENT ❌

```
Status: ❌ NOT STARTED
Path:   ./WebDev/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| **Frontend** |
| 8.1 | HTML/CSS | Semantic HTML, Flexbox, Grid, Responsive Design | ❌ |
| 8.2 | JavaScript Core | ES6+, DOM, Events, Fetch API, Web APIs | ❌ |
| 8.3 | React | Components, Hooks, State, Context, Redux, Next.js | ❌ |
| 8.4 | Performance | Lazy Loading, Code Splitting, Web Vitals, Caching | ❌ |
| 8.5 | Accessibility | ARIA, Screen Readers, WCAG, Keyboard Navigation | ❌ |
| **Backend** |
| 8.6 | Node.js / Express | REST APIs, Middleware, Authentication, Error Handling | ❌ |
| 8.7 | Spring Boot (Java) | MVC, JPA, Security, Microservices | ❌ |
| 8.8 | Django / FastAPI (Python) | ORM, REST Framework, Async Views | ❌ |
| 8.9 | Authentication | JWT, OAuth2, Session, SSO, RBAC | ❌ |
| 8.10 | API Design | REST Best Practices, Versioning, Documentation (Swagger) | ❌ |

---

## 9. DEVOPS & CLOUD ❌

```
Status: ❌ NOT STARTED
Path:   ./DevOps/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 9.1 | Linux & Shell | Commands, Scripting, Cron, SSH, File System | ❌ |
| 9.2 | Git & Version Control | Branching, Merging, Rebasing, Git Flow, Monorepo | ❌ |
| 9.3 | Docker | Containers, Dockerfile, Docker Compose, Images, Volumes | ❌ |
| 9.4 | Kubernetes | Pods, Services, Deployments, ConfigMaps, Helm, Ingress | ❌ |
| 9.5 | CI/CD | Jenkins, GitHub Actions, GitLab CI, Build Pipelines | ❌ |
| 9.6 | AWS Essentials | EC2, S3, RDS, Lambda, SQS, SNS, CloudFront, IAM | ❌ |
| 9.7 | GCP / Azure Basics | Compute, Storage, Networking equivalents | ❌ |
| 9.8 | Infrastructure as Code | Terraform, CloudFormation | ❌ |
| 9.9 | Monitoring | Prometheus, Grafana, ELK Stack, Datadog | ❌ |
| 9.10 | Networking & Security | VPC, Subnets, Security Groups, WAF, Secrets Management | ❌ |

---

## 10. SOFTWARE ENGINEERING PRACTICES ❌

```
Status: ❌ NOT STARTED
Path:   ./SoftwareEngineering/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 10.1 | SDLC | Waterfall, Agile, Scrum, Kanban, Sprint Planning | ❌ |
| 10.2 | Agile & Scrum | User Stories, Sprint, Retrospective, Velocity, Burndown | ❌ |
| 10.3 | Code Quality | Clean Code, Code Reviews, Linting, Static Analysis | ❌ |
| 10.4 | Testing | Unit, Integration, E2E, Load, Performance, A/B Testing | ❌ |
| 10.5 | Documentation | Technical Writing, ADRs, API Docs, Runbooks | ❌ |
| 10.6 | Estimation | Story Points, T-shirt Sizing, Planning Poker | ❌ |
| 10.7 | Technical Debt | Identifying, Measuring, Managing, Paying Off | ❌ |
| 10.8 | Software Architecture | Monolith vs Microservices, Event-Driven, Serverless, CQRS | ❌ |

---

## 11. SECURITY & CRYPTOGRAPHY ❌

```
Status: ❌ NOT STARTED
Path:   ./Security/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 11.1 | Web Security | OWASP Top 10, XSS, CSRF, SQL Injection, Clickjacking | ❌ |
| 11.2 | Authentication & Authorization | OAuth2, JWT, SAML, RBAC, ABAC | ❌ |
| 11.3 | Cryptography Basics | Symmetric (AES), Asymmetric (RSA), Hashing (SHA), Digital Signatures | ❌ |
| 11.4 | TLS/SSL | Handshake, Certificates, PKI | ❌ |
| 11.5 | Secure Coding | Input Validation, Output Encoding, Parameterized Queries | ❌ |
| 11.6 | API Security | Rate Limiting, API Keys, OAuth Scopes, CORS | ❌ |

---

## 12. BEHAVIORAL & SOFT SKILLS ❌

```
Status: ❌ NOT STARTED
Path:   ./Behavioral/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 12.1 | STAR Method | Situation, Task, Action, Result — Framework | ❌ |
| 12.2 | Leadership Stories | Conflict Resolution, Difficult Decisions, Mentoring | ❌ |
| 12.3 | Amazon Leadership Principles | Customer Obsession, Ownership, Bias for Action, etc. (16 principles) | ❌ |
| 12.4 | Google Values | Googleyness, Problem Solving, Collaboration | ❌ |
| 12.5 | Project Deep Dives | How to present past projects, architecture decisions | ❌ |
| 12.6 | Communication | Technical Communication, Whiteboard Presenting, Feedback | ❌ |
| 12.7 | Negotiation | Salary Negotiation, Offer Comparison, Counter-offers | ❌ |

---

## 13. AI / ML FUNDAMENTALS ❌

```
Status: ❌ NOT STARTED
Path:   ./AI-ML/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 13.1 | ML Basics | Supervised, Unsupervised, Reinforcement Learning | ❌ |
| 13.2 | Classic Algorithms | Linear Regression, Logistic Regression, Decision Trees, SVM, KNN, K-Means | ❌ |
| 13.3 | Deep Learning | Neural Networks, CNN, RNN, Transformers, Attention | ❌ |
| 13.4 | NLP | Tokenization, Embeddings, BERT, GPT, Sentiment Analysis | ❌ |
| 13.5 | LLM & GenAI | Prompt Engineering, RAG, Fine-tuning, Agents, LangChain | ❌ |
| 13.6 | MLOps | Model Serving, Monitoring, A/B Testing, Feature Stores | ❌ |
| 13.7 | Math for ML | Linear Algebra, Probability, Statistics, Calculus | ❌ |

---

## 14. COMPETITIVE PROGRAMMING ❌

```
Status: ❌ NOT STARTED
Path:   ./CompetitiveProgramming/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 14.1 | Number Theory | Primes, Modular Arithmetic, Euler's Totient, Chinese Remainder | ❌ |
| 14.2 | Combinatorics | Permutations, Combinations, Catalan Numbers, Inclusion-Exclusion | ❌ |
| 14.3 | Advanced DP | Bitmask DP, Digit DP, DP on Trees, DP with Optimization | ❌ |
| 14.4 | Graph Advanced | Network Flow, Bipartite Matching, Euler Path, Hamiltonian | ❌ |
| 14.5 | Geometry | Convex Hull, Line Intersection, Point in Polygon | ❌ |
| 14.6 | String Advanced | Suffix Array, Suffix Tree, Aho-Corasick, Z-Function | ❌ |

---

## 15. DISTRIBUTED SYSTEMS ❌

```
Status: ❌ NOT STARTED
Path:   ./DistributedSystems/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 15.1 | Fundamentals | Why Distributed?, Fallacies of Distributed Computing | ❌ |
| 15.2 | Consistency & Consensus | CAP Theorem, Raft, Paxos, 2PC, 3PC | ❌ |
| 15.3 | Replication | Single-Leader, Multi-Leader, Leaderless | ❌ |
| 15.4 | Partitioning | Hash, Range, Consistent Hashing | ❌ |
| 15.5 | Clocks & Ordering | Lamport Timestamps, Vector Clocks, NTP | ❌ |
| 15.6 | Transactions | ACID, BASE, Saga Pattern, 2PC vs Saga | ❌ |
| 15.7 | Storage Systems | LSM Trees, B+ Trees, SSTables, WAL | ❌ |
| 15.8 | Real Systems | Kafka, Cassandra, DynamoDB, Spanner, ZooKeeper | ❌ |

---

## 16. MOBILE DEVELOPMENT ❌

```
Status: ❌ NOT STARTED
Path:   ./Mobile/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 16.1 | Android (Kotlin) | Activity/Fragment, ViewModel, Compose, Room, Coroutines | ❌ |
| 16.2 | iOS (Swift) | UIKit, SwiftUI, Core Data, Combine, Concurrency | ❌ |
| 16.3 | React Native | Components, Navigation, State Management, Native Modules | ❌ |
| 16.4 | Flutter (Dart) | Widgets, State Management, Platform Channels | ❌ |
| 16.5 | Mobile System Design | Offline-first, Caching, Push Notifications, Deep Linking | ❌ |

---

## 17. MATHEMATICS FOR CS ❌

```
Status: ❌ NOT STARTED
Path:   ./Math/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 17.1 | Discrete Math | Sets, Relations, Functions, Logic, Proofs | ❌ |
| 17.2 | Probability & Statistics | Bayes, Distributions, Expected Value, Variance | ❌ |
| 17.3 | Linear Algebra | Vectors, Matrices, Eigenvalues, SVD | ❌ |
| 17.4 | Graph Theory | Euler/Hamiltonian, Coloring, Planar Graphs | ❌ |
| 17.5 | Complexity Theory | P, NP, NP-Complete, NP-Hard, Reductions | ❌ |

---

## 18. TOOLS & PRODUCTIVITY ❌

```
Status: ❌ NOT STARTED
Path:   ./Tools/
```

| # | Topic | Subtopics | Status |
|---|-------|-----------|--------|
| 18.1 | Git Mastery | Advanced Git, Rebase, Cherry-pick, Bisect, Hooks | ❌ |
| 18.2 | IDE & Editor | VS Code, IntelliJ, Vim, Shortcuts, Extensions | ❌ |
| 18.3 | Terminal & Shell | Bash, Zsh, tmux, Aliases, Scripting | ❌ |
| 18.4 | Debugging | Debugger, Profiling, Logging, Tracing | ❌ |
| 18.5 | Productivity | Note-taking, Time Management, Deep Work, Learning Techniques | ❌ |

---

## Study Priority (For Interviews)

| Priority | Topics | Why |
|----------|--------|-----|
| **P0 (Must)** | DSA, LLD, HLD | Asked in EVERY interview |
| **P1 (Critical)** | Database/SQL, OS, Networks | Asked in most interviews |
| **P2 (Important)** | Behavioral, Language Deep Dive | 1 round dedicated at most companies |
| **P3 (Good to Have)** | DevOps, Security, Web Dev | Role-specific, shows breadth |
| **P4 (Bonus)** | AI/ML, Distributed Systems, Mobile | Specialized roles only |

---

## Recommended Study Order

```
Week 1-4:   DSA Fundamentals (Arrays, Strings, Hashing, Trees, Graphs)
Week 5-8:   DSA Advanced (DP, Backtracking, Graph Algorithms)
Week 9-10:  LLD (already done! ✅ Review and practice)
Week 11-14: HLD / System Design
Week 15-16: Database & SQL
Week 17:    OS + Networks
Week 18:    Behavioral + Language Deep Dive
Week 19-20: Mock Interviews + Revision
```

---

> **Sources:**
> - [FAANG Job Prep 2026-2027 Roadmap](https://roadmap.swadhin.cv/)
> - [Complete FAANG Preparation (GitHub)](https://github.com/AkashSingh3031/The-Complete-FAANG-Preparation)
> - [Coding Interview University (GitHub)](https://github.com/jwasham/coding-interview-university)
> - [Tech Interview Handbook](https://www.techinterviewhandbook.org/software-engineering-interview-guide/)
> - [GeeksforGeeks CS Core Subjects](https://www.geeksforgeeks.org/tutorials/articles-on-computer-science-subjects-gq/)
> - [awesome-low-level-design (GitHub)](https://github.com/ashishps1/awesome-low-level-design)
