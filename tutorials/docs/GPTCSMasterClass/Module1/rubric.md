# Masterclass: Practical Computer Science for CNC Programmers

**Audience:** Experienced CNC machinist and self-taught programmer. Knows Python & JS, wants firm CS foundations, C++ DSA prep, better code structure, and applied low-level systems knowledge relevant to machining and automation.

**Goal:** Take you from "I can make code work" → professional engineer: readable, testable, maintainable systems across Python / JS / C++ / tooling. Deep focus on small code bites, hands-on mini-projects, refactors of legacy code (G-code/post-processors), and production-ready practices you can copy into mkdocs.

---

## How to use this repository

- Each module is self-contained markdown (mkdocs-ready). Copy a module file into your `docs/` folder and it will render in mkdocs-material.
- Every module follows a strict template so you can pick it up day-by-day:

  - **Duration:** suggested timebox (short / medium / deep)
  - **Prereqs:** what you should already know
  - **Objectives:** concrete learnable outcomes (3–6)
  - **Lessons:** short bite-sized lessons; each lesson has 1–4 _code bites_ (copy/paste + explain)
  - **Mini project:** small hands-on build that ties lessons together
  - **Exercises / Challenges:** progressive problems with increasing difficulty
  - **Deliverables & Tests:** what to commit — includes unit tests where relevant
  - **MkDocs frontmatter template** so you can paste directly into `docs/module-XX.md`

### MkDocs file frontmatter (copy into the top of any module file)

```yaml
---
title: "Module 01 — Course orientation & dev environment"
description: "Quick setup and course workflow: git, editors, containerization"
---
```

---

## Curriculum structure (60 modules)

The course is grouped into **7 sections**. Each module below is short and actionable; modules include small code snippets and a mini-project at the end.

> **Section A — Foundations & Tooling (Modules 1–8)**

### Module 01 — Course orientation & dev environment

- **Duration:** short
- **Prereqs:** basic comfort with a terminal
- **Objectives:** Git basics, VSCode + useful extensions, WSL/Terminal setup, Python & Node version managers, Docker quickstart
- **Mini project:** Create a repo with a reproducible dev container (Dockerfile) and a run script.

### Module 02 — Shell, awk, sed, and automation tools

- **Duration:** short
- **Objectives:** Practical one-liners, AWK for text transformation, sed for in-place edits, make and simple Makefiles, tmux workflow
- **Mini project:** Build a Makefile that builds, lints, and runs tests for a small Python project.

### Module 03 — Advanced Git & workflows

- **Duration:** medium
- **Objectives:** Branching strategies, rebase vs merge, bisect, hooks, signed commits, git submodules and subtrees
- **Mini project:** Create a git-hook that enforces a commit message template and runs unit tests pre-push.

### Module 04 — Editor ergonomics & debugging toolchain

- **Duration:** short
- **Objectives:** VSCode tips, debugger setups (Python/Node/C++), using LSPs, using ripgrep and code search, editorconfig
- **Mini project:** Configure a workspace that debugs a Python FastAPI app with hot-reload.

### Module 05 — Programming hygiene & style (clean code)

- **Duration:** medium
- **Objectives:** SOLID, separation of concerns, naming conventions, idiomatic Python/JS/C++ style, linting, formatting, pre-commit
- **Mini project:** Lint and refactor a small messy script into a testable module with clear API.

### Module 06 — Testing fundamentals (unit/integration/TDD)

- **Duration:** medium
- **Objectives:** Pytest, jest, writing mocks, property-based testing, test design, CI integration
- **Mini project:** TDD a small parser for a subset of G-code lines.

### Module 07 — Package & dependency management

- **Duration:** short
- **Objectives:** Python packaging (venv, pip, pyproject/poetry), npm/yarn, C++ dependency basics (vcpkg/conan), reproducible builds
- **Mini project:** Publish a tiny Python package to TestPyPI and install it from a clean venv.

### Module 08 — Containerization basics (Docker)

- **Duration:** medium
- **Objectives:** Images, layers, Dockerfile best practices, multi-stage builds, compose, local dev containers
- **Mini project:** Containerize a microservice and compose it with a DB for local integration testing.

> **Section B — Core Programming (Modules 9–20)**

### Module 09 — Python deep-dive: internals & idioms

- **Duration:** medium
- **Objectives:** Data model, descriptors, **slots**, iterators, generators, decorators, context managers
- **Mini project:** Implement a streaming G-code transformer using generators and context managers.

### Module 10 — JavaScript deep-dive: event loop & async

- **Duration:** medium
- **Objectives:** Event loop, microtasks vs macrotasks, promises, async/await, memory leaks
- **Mini project:** Build a Node script that streams a large CSV and posts chunks to a test endpoint.

### Module 11 — TypeScript & robust typing

- **Duration:** short
- **Objectives:** Type system, generics, declaration files, migrating JS → TS incrementally
- **Mini project:** Convert a small JS utility library to TypeScript with types and tests.

### Module 12 — C++ refresher: build, compile, link

- **Duration:** short
- **Objectives:** Toolchain (g++, clang), compilation units, headers vs implementation, static vs dynamic linking
- **Mini project:** Build a CLI that reads G-code and prints simplified tokens.

### Module 13 — Modern C++: RAII, smart pointers, move semantics

- **Duration:** medium
- **Objectives:** unique_ptr, shared_ptr, move ctor/assignment, value categories
- **Mini project:** Implement a small resource manager class for a mock machine connection.

### Module 14 — Data structures 1: arrays, lists, stacks, queues

- **Duration:** medium
- **Objectives:** Implementations, complexity, memory layout, when to pick which structure
- **Mini project:** Implement a ring buffer (circular queue) in C++ and Python and benchmark.

### Module 15 — Data structures 2: trees & graphs

- **Duration:** medium
- **Objectives:** Binary trees, BST, AVL, graph representations, traversals
- **Mini project:** Build a simple dependency graph for machining steps and topologically sort it.

### Module 16 — Hashing & maps

- **Duration:** short
- **Objectives:** Hash functions, collisions, practical implementations, python dict internals, unordered_map in C++
- **Mini project:** Implement a small cache with LRU eviction.

### Module 17 — Algorithms I: sorting & searching

- **Duration:** short
- **Objectives:** Sorting algorithms, complexity, practical considerations; binary search patterns
- **Mini project:** Compare std::sort vs custom quicksort for different data shapes.

### Module 18 — Algorithms II: graphs & DP

- **Duration:** medium
- **Objectives:** Dijkstra, BFS/DFS, DP patterns and memoization
- **Mini project:** Find the shortest toolpath on a simple grid with weightings.

### Module 19 — Complexity & proofs (Big-O rigorous)

- **Duration:** short
- **Objectives:** Formal reasoning about time/space, amortized analysis, lower bounds
- **Mini project:** Analyze and document complexity of a post-processor pipeline.

### Module 20 — Low-level data formats & serialization

- **Duration:** short
- **Objectives:** JSON/YAML, binary formats, Protobuf, endianness
- **Mini project:** Design a compact binary format to stream G-code meta-data between services.

> **Section C — Systems, Concurrency & Networking (Modules 21–32)**

### Module 21 — Networking basics: sockets, TCP/UDP

- **Duration:** medium
- **Objectives:** Sockets API, stream vs datagram, timeouts, partial reads
- **Mini project:** Build a small TCP server that accepts G-code lines and acknowledges parsing.

### Module 22 — Concurrency: threads & async

- **Duration:** medium
- **Objectives:** Thread safety, locks, atomics, asyncio, async in C++ (std::future, coroutines)
- **Mini project:** Convert a blocking parser into an async streaming parser that writes parsed events.

### Module 23 — Real-time & low-latency considerations

- **Duration:** medium
- **Objectives:** Real-time constraints, jitter, priority queues, OS scheduling basics
- **Mini project:** Simulate a simple motion planner that respects deadlines.

### Module 24 — IPC & messaging patterns

- **Duration:** short
- **Objectives:** Pipes, shared memory, message queues, pub/sub, ZeroMQ, MQTT for shop-floor telemetry
- **Mini project:** Implement a telemetry pub/sub pipeline between mock controller and dashboard.

### Module 25 — System design fundamentals

- **Duration:** medium
- **Objectives:** Modularity, separation of concerns, API boundaries, scalability tradeoffs
- **Mini project:** Architect a post-processor microservice with clear boundaries.

### Module 26 — Embedded basics & hardware interfacing

- **Duration:** medium
- **Objectives:** Serial protocols, GPIO basics, reading encoders, controlling stepper/servo (conceptual)
- **Mini project:** Create a mocked serial driver and integration tests that simulate machine responses.

### Module 27 — G-code parsing & interpreters (applied parser design)

- **Duration:** medium
- **Objectives:** Lexer → parser → AST → codegen, incremental parsing, streaming tokens, error recovery
- **Mini project:** Build a 3-stage pipeline: lexer, parser, optimizer for a G-code subset.

### Module 28 — File formats, compression, and storage patterns

- **Duration:** short
- **Objectives:** Filesystems, chunked storage, compression techniques (gzip, lz4), streaming files
- **Mini project:** Implement chunked upload/download of large job files with resume support.

### Module 29 — Observability: logging, metrics, tracing

- **Duration:** short
- **Objectives:** Structured logging, OpenTelemetry basics, Prometheus metrics, tracing flows for async systems
- **Mini project:** Add tracing and metrics to a small FastAPI job-queue service.

### Module 30 — Debugging & profiling (practical)

- **Duration:** medium
- **Objectives:** Profilers (perf, py-spy), memory leaks, core dumps, heuristics for hotspots
- **Mini project:** Profile a parsing pipeline and optimize the top 2 hotspots.

### Module 31 — Build systems: Make, CMake, and reproducible builds

- **Duration:** medium
- **Objectives:** CMake patterns, cross-compilation basics, hermetic builds
- **Mini project:** Write a CMake config for the C++ parser and integrate into CI.

### Module 32 — Continuous Integration & delivery basics

- **Duration:** medium
- **Objectives:** GitHub Actions, pipelines, test matrices, release artifacts
- **Mini project:** CI workflow that runs unit tests, builds artifacts, and publishes a release candidate.

> **Section D — Databases, Storage & Persistence (Modules 33–38)**

### Module 33 — Relational databases & SQL (Postgres)

- **Duration:** medium
- **Objectives:** Schema design, indexes, transactions, ACID, explain analyze
- **Mini project:** Design a schema for job management and write queries for common patterns.

### Module 34 — NoSQL & time-series storage

- **Duration:** short
- **Objectives:** Document stores, when to use, time-series DBs for telemetry
- **Mini project:** Store telemetry stream in a time-series DB and plot metrics.

### Module 35 — ORMs and migrations (practical patterns)

- **Duration:** short
- **Objectives:** SQLAlchemy, Alembic, migration patterns, pitfalls
- **Mini project:** Implement migrations for a schema change and write a compatibility test.

### Module 36 — Filesystems & large file handling

- **Duration:** short
- **Objectives:** Streaming, chunking, S3 patterns, consistency models
- **Mini project:** Implement S3-compatible chunked upload + index for quick seeking.

### Module 37 — Search & indexing basics

- **Duration:** short
- **Objectives:** Full-text search basics, inverted indexes, practical use cases
- **Mini project:** Add a simple search index over job metadata with ranked results.

### Module 38 — Backups, snapshots & disaster recovery

- **Duration:** short
- **Objectives:** Backup strategies, point-in-time recovery, retention policies
- **Mini project:** Scripted backup/restore for a small Postgres instance.

> **Section E — Software Design, Patterns & Refactoring (Modules 39–46)**

### Module 39 — Refactoring legacy code & anti-patterns

- **Duration:** medium
- **Objectives:** Identifying smells, incremental refactor, safety nets (tests, feature flags)
- **Mini project:** Take a small messy post-processor script and refactor to modules + tests.

### Module 40 — Design patterns in practice

- **Duration:** medium
- **Objectives:** Factory, Strategy, Visitor, Adapter — with examples in Python and C++
- **Mini project:** Use Visitor pattern to implement an AST transformer for G-code optimizations.

### Module 41 — Modular monoliths vs microservices

- **Duration:** medium
- **Objectives:** When to split, coupling vs cohesion, data ownership, transaction patterns
- **Mini project:** Split a monolith into two services (parser + executor) and wire with a queue.

### Module 42 — API design, versioning, and backward compatibility

- **Duration:** short
- **Objectives:** Semantic versioning, API versioning strategies, graceful evolution
- **Mini project:** Add versioned endpoints and write migration compatibility tests.

### Module 43 — Event-driven architectures & CQRS basics

- **Duration:** medium
- **Objectives:** Event sourcing basics, command-query separation, idempotency
- **Mini project:** Implement an event-sourced job-state store with replay capability.

### Module 44 — Observability applied to manufacturing systems

- **Duration:** short
- **Objectives:** Machine telemetry best practices, health checks, alerting
- **Mini project:** Build a dashboard that consumes metrics and raises alerts on thresholds.

### Module 45 — Secure coding & authentication

- **Duration:** short
- **Objectives:** Authentication (JWT/OAuth), secrets management, secure defaults, least privilege
- **Mini project:** Harden a small service with token-based auth and secret rotation.

### Module 46 — Performance engineering & benchmarking

- **Duration:** medium
- **Objectives:** Microbenchmarks vs macro, representative workloads, benchmarking tools
- **Mini project:** Create a benchmark suite for throughput and latency of parsing pipeline.

> **Section F — Frontend, Visualization & UX (Modules 47–52)**

### Module 47 — Frontend fundamentals: DOM, accessibility, and performance

- **Duration:** short
- **Objectives:** Accessibility, semantic HTML, rendering performance
- **Mini project:** Build a G-code viewer that renders lines and supports keyboard navigation.

### Module 48 — React from first principles

- **Duration:** medium
- **Objectives:** Virtual DOM, reconciliation, hooks, memoization
- **Mini project:** Implement a React-based G-code visualizer with playback controls.

### Module 49 — State management & data fetching

- **Duration:** short
- **Objectives:** Local state, global store patterns, caching strategies, optimistic updates
- **Mini project:** Add job-state caching with stale-while-revalidate semantics.

### Module 50 — Data visualization & charts

- **Duration:** short
- **Objectives:** Efficient rendering for large data sets, canvas vs SVG, streaming charts
- **Mini project:** Build a streaming chart showing telemetry for a running job.

### Module 51 — UX for industrial software

- **Duration:** short
- **Objectives:** Minimal interfaces, error recovery flows, user safety, keyboard-first UI
- **Mini project:** Design a safe confirmation and undo flow for destructive job operations.

### Module 52 — Testing frontends: E2E & unit

- **Duration:** short
- **Objectives:** Jest, Playwright, component testing, accessibility testing
- **Mini project:** Add E2E tests that validate a job upload → parse → visualize flow.

> **Section G — Advanced topics, capstones & career prep (Modules 53–60)**

### Module 53 — Distributed systems & scaling fundamentals

- **Duration:** medium
- **Objectives:** Consistency models, consensus basics, partitioning strategies
- **Mini project:** Shard a simple job-store and demonstrate requests routing.

### Module 54 — Kubernetes essentials for developers

- **Duration:** medium
- **Objectives:** Pods, services, deployments, configmaps, secrets, basic k8s debugging
- **Mini project:** Deploy the parser + API to a local k8s cluster (kind/minikube).

### Module 55 — Numerical methods, precision, and stability

- **Duration:** medium
- **Objectives:** Floating point, rounding errors, stable algorithms, fixed-point math for controllers
- **Mini project:** Implement fixed-point interpolation and compare to floating-point.

### Module 56 — Signal processing & sensor fusion basics

- **Duration:** medium
- **Objectives:** Filters (low-pass, Kalman concept), sampling theory, aliasing
- **Mini project:** Build a filter that smooths noisy encoder readings and test against synthetic noise.

### Module 57 — Automation & scripting for toolchains

- **Duration:** short
- **Objectives:** Scripting CI releases, auto-deploys, job scheduling patterns
- **Mini project:** Create a release pipeline that tags, builds artifacts, and publishes.

### Module 58 — Capstone 1: CNC microservice stack

- **Duration:** deep
- **Objectives:** End-to-end service: uploader → parser → optimizer → executor simulator + dashboard
- **Deliverable:** Production-quality repo with CI, tests, docs, and deployable artifacts.

### Module 59 — Capstone 2: G-code visualizer & post-processor

- **Duration:** deep
- **Objectives:** Full-stack product: parsing, optimization passes, UI playback, and export
- **Deliverable:** Deployable app and write a technical postmortem describing design choices.

### Module 60 — Career, growth, and next steps

- **Duration:** short
- **Objectives:** Interview prep plan (DSA + system design), code review best practices, mentoring others
- **Mini project:** Mock interview plan + coding problems and system-design checklist.

---

## Delivery mechanics & daily/weekly cadence

- **Micro-sessions:** 30–90 minutes each lesson. Code bites are intentionally short (5–30 lines) and explained line-by-line.
- **Weekly plan suggestion:** 3 modules/week for 20 weeks (standard), or 1 module/day for an accelerated month (intense).
- **Review & spaced repetition:** Every 5th module is a short review + consolidation mini-project.

## How I will support you here

- I created this full course as a set of markdown modules in this document. Tell me which module number you want to _open next_ and I will:

  1. Expand that module into a step-by-step lesson plan in this chat (with code snippets, tests, and exercises).
  2. Produce a single mkdocs-ready markdown file you can copy into `docs/module-XX.md`.
  3. If you want, I can walk you through running each mini-project locally and help debug issues you hit.

---

### Closing notes

This curriculum is intentionally pragmatic: it focuses on the intersection of CS fundamentals and real-world problems you face as a CNC machinist — parsing G-code, building robust pipelines, and shipping maintainable software. Pick a module and let's start building.
