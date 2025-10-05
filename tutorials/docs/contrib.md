Great — I’ll give you **Stage 0**: a beginner-friendly, deep-practice primer that builds the mental models and tiny coding steps you need before we dive into `create_task`, `gather`, thread pools, FastAPI, etc. Type the short snippets yourself, run them, and read the explanations and side notes as you go. I’ll also point to authoritative resources for each big idea.

**Stage 0 goals (what you’ll be able to do after this):**

- Explain the difference between _concurrency_ and _parallelism_ and when each matters.
- Explain _blocking_ vs _non-blocking_ behavior and why that matters for servers.
- Understand the core async primitives in Python: **event loop**, **coroutine**, **Task**, **Future**, `await`.
- Know when to use thread/process pools (and why the GIL matters).
- Run small examples showing the different behaviors and measure them.
- Complete simple practice exercises to solidify the mental model.

I’ll keep each concept short + runnable. Ready? Stage 0 — go.

---

# 1) Mental model first — analogies you’ll rely on

**Concurrency vs Parallelism (simple):**

- _Concurrency_ = “many things in progress” (one cook juggles multiple dishes by switching between them).
- _Parallelism_ = “many things at the same time” (multiple cooks, each on a different stove).

**Blocking vs Non-blocking:**

- _Blocking_ = the cook stands at the stove and waits for water to boil; nothing else gets done.
- _Non-blocking_ = the cook starts the kettle, then goes to chop vegetables while the kettle heats.

Why this matters: web servers that handle lots of network I/O get much better throughput if they don’t block while waiting for network or disk I/O. (More formal coverage: Python concurrency docs.) ([Python documentation][1])

---

# 2) Key definitions (short) — the vocabulary you’ll use

- **Event loop** — the scheduler that runs coroutines and decides "who runs next." In Python this is `asyncio`'s loop. ([Python documentation][2])
- **Coroutine** — an `async def` function in Python. Calling it produces a coroutine object (a unit of work the loop can run). The `async`/`await` syntax was standardized by PEP 492. ([Python Enhancement Proposals (PEPs)][3])
- **Task** — a coroutine that has been scheduled on the loop (usually via `asyncio.create_task`); it will run concurrently with other tasks. See docs on coroutines & tasks. ([Python documentation][4])
- **Future** — low-level object representing “a value that will exist later”; Tasks are Futures with extra scheduling semantics.
- **ThreadPoolExecutor / ProcessPoolExecutor** — run blocking (or CPU-bound) work in separate threads/processes to avoid blocking the event loop. Use `concurrent.futures` for that. ([Python documentation][5])

---

# 3) Quick JS → Python map (so the different languages line up)

- JavaScript `async function` / `await` ⇄ Python `async def` / `await`. Both are syntactic sugar for promise/coroutine-based concurrency. (For JS reference see MDN.) ([MDN Web Docs][6])
- `fetch()` + `.then()` maps to `await client.get()` in Python async libraries. The event-loop idea is similar (JS runtime event loop vs Python’s `asyncio` loop).

---

# 4) Tiny runnable examples — type these and run them

**A — blocking (type and run as `python step_blocking.py`)**

```py
# step_blocking.py
import time

def blocking_task(name, s):
    print(f"{name} start")
    time.sleep(s)   # blocks whole thread
    print(f"{name} done")

def main():
    t0 = time.time()
    blocking_task("A", 2)
    blocking_task("B", 1)
    print("Elapsed", time.time()-t0)

if __name__ == "__main__":
    main()
```

Expected: ~3s total — tasks run one after the other.

**Why to type this:** see how `time.sleep` halts everything.

---

**B — non-blocking coroutines (type as `python step_async.py`)**

```py
# step_async.py
import asyncio
import time

async def coro(name, s):
    print(f"{name} start")
    await asyncio.sleep(s)   # yields to event loop
    print(f"{name} done")

async def main():
    t0 = time.time()
    await asyncio.gather(coro("C", 2), coro("D", 1))
    print("Elapsed", time.time()-t0)

if __name__ == "__main__":
    asyncio.run(main())
```

Expected: ~2s total — tasks overlapped by the event loop.

**Why to type this:** `asyncio.sleep` yields control and lets the other coroutine proceed — you _gain concurrency_ without threads.

Reference: official asyncio quick example. ([Python documentation][2])

---

# 5) Deep dive: `await`, coroutine objects, Tasks, `create_task`, `gather`

**What `await` does**

- `await` suspends the current coroutine until the awaited awaitable resolves. While suspended, the event loop can run other tasks. This is _cooperative multitasking_.

**Coroutines vs Tasks**

- `async def f(): ...` → `c = f()` produces a coroutine object (nothing runs yet).
- `await c` — runs that coroutine and waits for it to finish.
- `t = asyncio.create_task(f())` — schedules the coroutine to run _in the background_ immediately and returns an `asyncio.Task` object. The loop will run it even if you don’t `await` it right away (but you should usually await or otherwise manage tasks).

**create_task vs gather (mental model)**

- `create_task` = _spawn_: start now, keep a handle to control/cancel it.
- `gather` = _start and wait for a bunch at once_: handy when you want to wait for multiple results.

Small snippet to feel the difference — type this and run:

```py
# step_task_demo.py
import asyncio

async def child(n):
    print("child", n, "start")
    await asyncio.sleep(n)
    print("child", n, "done")
    return n * 10

async def main():
    # spawn tasks (they start immediately)
    t1 = asyncio.create_task(child(2))
    t2 = asyncio.create_task(child(1))

    print("spawned tasks; doing other work")
    await asyncio.sleep(0.1)
    # wait for both results
    res = await asyncio.gather(t1, t2)
    print("results:", res)

asyncio.run(main())
```

Watch the ordering and the returned `results`.

Docs and conceptual overview on tasks: official asyncio HowTo and task docs. ([Python documentation][4])

---

# 6) When to use `run_in_executor` / ThreadPoolExecutor / ProcessPoolExecutor

**Rule of thumb:**

- Use async/await when your program is _I/O-bound_: network, database, file reads (waiting happens often). `asyncio` lets many tasks share a single thread effectively. ([Python documentation][2])
- If you have _CPU-bound_ work (heavy computation), async won’t help because the CPU stays busy — use a process pool or native code that releases the GIL.

**What the GIL means (brief):**

- CPython’s Global Interpreter Lock (GIL) means only one thread executes Python bytecode at once — this limits multi-threaded parallel CPU gains in pure Python. For I/O-bound threaded programs threads can still help because while one thread waits (I/O), another runs. (Good explainer: Real Python on the GIL.) ([Real Python][7])

**Example: run blocking function on threads (type and run)**

```py
# step_executor.py
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def blocking_io(n):
    print("blocking start", n)
    time.sleep(n)
    print("blocking end", n)
    return n

async def main():
    loop = asyncio.get_running_loop()
    # Option A: default thread pool
    fut = loop.run_in_executor(None, blocking_io, 2)
    # Option B: custom ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=2) as ex:
    #     fut = loop.run_in_executor(ex, blocking_io, 2)
    res = await fut
    print("result:", res)

asyncio.run(main())
```

**Why this helps:** `blocking_io` runs in another thread so the event loop can continue scheduling other coroutines.

Docs: `concurrent.futures.ThreadPoolExecutor`. ([Python documentation][5])

---

# 7) Small experiments to type (practice now)

**Exercise A (type):** Convert the `blocking_task` example into an async version and measure elapsed time (you already did this in B — but do it manually and explain each line).

**Exercise B (type & explore):** Remove the `await` from `await asyncio.sleep()` in the coroutine and run — what happens? (Hint: coroutine returns a coroutine object; nothing runs until awaited.)

**Exercise C (type & test):** Use `create_task` to start 3 coroutines but cancel one before it completes. Observe `CancelledError`. Example:

```py
# cancel_test.py
import asyncio

async def worker(n):
    try:
        print("worker", n, "start")
        await asyncio.sleep(5)
        print("worker", n, "done")
    except asyncio.CancelledError:
        print("worker", n, "was cancelled")
        raise

async def main():
    t = asyncio.create_task(worker(1))
    await asyncio.sleep(1)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("confirmed cancel")

asyncio.run(main())
```

**Exercise D (type & run):** Implement a concurrency limit using `asyncio.Semaphore` — allow only 2 concurrent writers simulating network calls (use `asyncio.sleep`).

---

# 8) Short troubleshooting checklist (common beginner mistakes)

- **Forgot to `await`** a coroutine → you get a coroutine object, nothing executes.
- **Used `time.sleep` inside async code** → blocks the loop; use `await asyncio.sleep` for testing.
- **Called `asyncio.run()` inside already running loop (e.g., IPython)** — it errors; use `await` directly inside IPython or create a new nested solution.
- **Left tasks unmanaged** (spawned with `create_task` and never awaited or canceled) — can lead to tasks running in background or errors at shutdown.
- **Expecting async to make CPU-bound code faster** — it won’t unless you offload to processes or C extensions.

---

# 9) Quick resources (authoritative + practical) — start here

- Python official `asyncio` library docs (tutorial & how-to). ([Python documentation][2])
- PEP 492 — explanation of `async` / `await` semantics. ([Python Enhancement Proposals (PEPs)][3])
- `concurrent.futures` (ThreadPoolExecutor & ProcessPoolExecutor docs). ([Python documentation][5])
- MDN: JavaScript async/await (good to compare JS mental model). ([MDN Web Docs][6])
- Real Python: Asyncio hands-on walkthrough (practical guide & exercises). ([Real Python][8])

(If you want, I’ll assemble these links into a printable one-pager you can keep beside your keyboard.)

---

# 10) Stage 0 exercises + brief solutions (run and check)

**Exercise 1 — Blocking vs async (what to type)**

- Type `step_blocking.py` and `step_async.py` (sections A and B above). Confirm blocking runs ~3s and async ~2s.

**Exercise 2 — Forgot-to-await**

```py
import asyncio

async def say():
    print("hello")
    await asyncio.sleep(0.1)
    print("bye")

c = say()
print("coroutine object:", c)
# run:
asyncio.run(say())   # correct
```

**Expected:** printing the coroutine object, then `hello`/`bye` when properly awaited.

**Exercise 3 — run_in_executor quick**
Type `step_executor.py` above and see that `blocking_io` runs, but loop remains responsive.

**Exercise 4 — Semaphore concurrency**

```py
import asyncio, time

async def job(i, sem):
    async with sem:
        print("start", i)
        await asyncio.sleep(1)
        print("end", i)

async def main():
    sem = asyncio.Semaphore(2)
    t0 = time.time()
    await asyncio.gather(*(job(i, sem) for i in range(6)))
    print("took", time.time()-t0)

asyncio.run(main())
```

**Expected:** because 2 run at a time and each takes 1s, total ≈ 3s.

---

# 11) End of Stage 0 — what Stage 1 will cover

If you finished Stage 0 comfortably, Stage 1 will expand to:

- Real HTTP examples (using `httpx` and `aiohttp`), mapping to `fetch` in JS.
- Cancellation patterns and proper cleanup (`asyncio.shield`, context managers for tasks).
- TaskGroups and structured concurrency (`asyncio.TaskGroup` in 3.11+).
- Advanced pools and when to prefer `ProcessPoolExecutor` vs `ThreadPoolExecutor`.
- Building a tiny FastAPI app demonstrating `async def` endpoint which hits an async DB (or simulates one).

---

If you want now, I can:

1. Turn **Stage 0** into a single printable Markdown file (tutorial + exercises + expected outputs).
2. Immediately give **Stage 1** here and start the practical HTTP + FastAPI examples.
3. Produce short screencast-style step-by-step commands (`what to type`, `what to run`, `what to expect`) for Stage 1.

Which of those next steps would you like?

[1]: https://docs.python.org/3/library/concurrency.html?utm_source=chatgpt.com "Concurrent Execution — Python 3.13.7 documentation"
[2]: https://docs.python.org/3/library/asyncio.html?utm_source=chatgpt.com "asyncio — Asynchronous I/O"
[3]: https://peps.python.org/pep-0492/?utm_source=chatgpt.com "PEP 492 – Coroutines with async and await syntax"
[4]: https://docs.python.org/3/library/asyncio-task.html?utm_source=chatgpt.com "Coroutines and Tasks"
[5]: https://docs.python.org/3/library/concurrent.futures.html?utm_source=chatgpt.com "concurrent.futures — Launching parallel tasks"
[6]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function?utm_source=chatgpt.com "async function - JavaScript | MDN - Mozilla"
[7]: https://realpython.com/python-gil/?utm_source=chatgpt.com "What Is the Python Global Interpreter Lock (GIL)?"
[8]: https://realpython.com/async-io-python/?utm_source=chatgpt.com "Python's asyncio: A Hands-On Walkthrough"

# Stage 1 — Foundations, clear beginner definitions, and runnable examples

Nice — we’ll treat Stage 1 as a practical _foundation_ that fills the gaps left by Stage 0. I’ll define every unusual term you’re likely to meet, give a short beginner-friendly definition _and_ a short technical note, show you 1–2 tiny runnable examples for each core idea, and give exercises with solutions you can type yourself. At the end I’ll say what Stage 2 will dig into (internals, scheduling, CPython/GIL, Task/Future internals, and so on).

> Read this slowly and _type_ the short snippets into files or a REPL. Typing helps build muscle memory. I’ll mark expected outputs and timing hints so you can confirm things worked.

---

# Goals for Stage 1

- You will _understand_ (not just memorize) the core vocabulary: coroutine, coroutine object, awaitable, await, Task, Future, event loop, create_task, gather, run_in_executor, ThreadPoolExecutor/ProcessPoolExecutor, semaphore, cancellation, TaskGroup, blocking vs non-blocking, I/O-bound vs CPU-bound, and structured concurrency.
- You will be able to _type and run_ simple programs that show the differences between sequential, concurrent (cooperative), and parallel approaches.
- You’ll be ready for Stage 2 where we open the hood and explain how Python schedules and implements these primitives.

---

# Core terms (Stage 1 definitions — beginner → short technical note)

I’ll use the pattern: **Beginner definition** → _Technical note / why it matters_ → `short example`.

1. **Coroutine**

   - Beginner: a special function you can pause and resume (`async def ...`).
   - Technical note: calling an `async def` function returns a _coroutine object_ (no code runs until you `await` it or schedule it). Coroutines are the units of work the event loop runs.
   - Example:

     ```py
     async def greet():
         print("hi")
         await asyncio.sleep(0.5)
         print("bye")
     ```

   - Stage 2: we’ll show how coroutines are implemented as state machines and how `await` transforms to `send()`/`yield` under the hood.

2. **Coroutine object**

   - Beginner: the thing you get when you call a coroutine function (e.g., `c = greet()`).
   - Technical note: a coroutine object is awaitable and has internal state (suspended, running, done). Nothing executes until it’s awaited or turned into a Task.
   - Example:

     ```py
     c = greet()
     print(type(c))  # <class 'coroutine'>
     ```

3. **Awaitable / `await`**

   - Beginner: `await` is how you _pause_ a coroutine until something finishes (e.g., I/O). The thing you `await` is an awaitable (another coroutine, Task, or Future).
   - Technical note: `await` yields control to the event loop and suspends execution until the awaited awaitable resolves.
   - Example: `result = await some_coroutine()`.

4. **Event loop**

   - Beginner: the scheduler that runs coroutines — think of it as the “conductor” of asynchronous tasks.
   - Technical note: it manages when to resume suspended coroutines, schedules callbacks, runs I/O watchers, and handles timers. `asyncio.get_running_loop()` returns the current loop.
   - Example usage: `asyncio.run(main())` creates/uses an event loop.

5. **Task**

   - Beginner: a scheduled coroutine that the loop will run concurrently with other tasks. You usually create one with `asyncio.create_task(...)`.
   - Technical note: a `Task` is a subclass of `Future` that wraps a coroutine and controls its execution. Tasks are what actually run on the loop.
   - Example:

     ```py
     t = asyncio.create_task(greet())
     ```

6. **Future**

   - Beginner: a placeholder for a value that will exist later.
   - Technical note: low-level primitive representing “result or exception at some point.” Tasks are higher-level Futures that wrap coroutines. You rarely create plain Futures unless building libraries.

7. **`create_task` vs `await`**

   - Beginner: `await foo()` runs `foo` and waits for it; `create_task(foo())` starts `foo` running in the background immediately and gives you a handle (Task).
   - Technical note: `create_task` schedules the coroutine on the loop; `await` runs it to completion inline (sequentially) if not previously scheduled.
   - Example:

     ```py
     t = asyncio.create_task(work(2))  # starts now
     # do something else
     await t  # wait for result later
     ```

8. **`gather`**

   - Beginner: a convenience to wait for multiple awaitables at once and collect results.
   - Technical note: `await asyncio.gather(a, b)` schedules `a` and `b` if they aren’t scheduled already, and waits for both to finish. If one raises, `gather` raises (there are options to change behavior).
   - Example: `results = await asyncio.gather(task1, task2)`.

9. **`run_in_executor` / ThreadPoolExecutor / ProcessPoolExecutor**

   - Beginner: a way to run blocking or CPU-heavy code without freezing the event loop. Threads or processes do the work while the loop stays responsive.
   - Technical note: `loop.run_in_executor(None, func, *args)` uses the default threadpool. `ProcessPoolExecutor` is used to bypass the GIL for CPU-bound tasks.
   - Example:

     ```py
     res = await loop.run_in_executor(None, blocking_io, arg)
     ```

10. **Blocking vs Non-blocking**

    - Beginner: _Blocking_ stops the whole thread (e.g., `time.sleep`); _non-blocking_ yields control (e.g., `await asyncio.sleep`).
    - Technical note: blocking calls must be moved off the event loop (threads/processes) to avoid freezing concurrency.

11. **I/O-bound vs CPU-bound**

    - Beginner: I/O-bound tasks spend time waiting (network/disk). CPU-bound tasks do heavy computation. Async helps the former much more than the latter.
    - Technical note: for CPU-bound in Python use `ProcessPoolExecutor` or native extensions that release the GIL.

12. **Cancellation & `CancelledError`**

    - Beginner: you can ask a Task to stop (`t.cancel()`); the coroutine receives a `CancelledError` to allow cleanup.
    - Technical note: cancellation is cooperative — coroutine must handle `CancelledError` if it needs to clean up.

13. **Semaphore**

    - Beginner: a counter that limits how many coroutines can run a section at the same time — great for concurrency limits.
    - Example:

      ```py
      sem = asyncio.Semaphore(3)
      async with sem:
          await do_io()
      ```

14. **Structured concurrency / TaskGroup (3.11+)**

    - Beginner: a safer way to start and manage multiple tasks together — they live and die together in a scope.
    - Technical note: `asyncio.TaskGroup` cancels all child tasks if one fails; this avoids “lost background tasks.”

15. **Async context manager / async iterator**

    - Beginner: `async with` and `async for` are the async versions of context managers/iterators. Useful for streams, sockets, async resources.
    - Example:

      ```py
      async with some_async_resource() as r:
          await r.do_stuff()
      ```

16. **Backpressure**

    - Beginner: when producers generate data faster than consumers can handle it; you must apply flow control (queues, semaphores).
    - Technical note: async streams/queues plus `await` let consumers apply backpressure by controlling when they `await` new items.

---

# Short runnable examples (type them and run)

> Tip: create files `s1_coroutine.py`, `s1_task_vs_await.py`, `s1_executor.py`, `s1_semaphore.py`. I show expected output and timing.

### Example A — Coroutine object vs awaiting

```py
# s1_coroutine.py
import asyncio

async def greet():
    print("hello")
    await asyncio.sleep(0.3)
    print("bye")

# calling returns coroutine object (nothing runs)
c = greet()
print("type:", type(c))   # coroutine object
# run it properly:
asyncio.run(greet())
```

Expected: prints the type, then `hello` / `bye`.

### Example B — sequential vs concurrent (gather / create_task)

```py
# s1_task_vs_await.py
import asyncio, time

async def work(n):
    print("start", n)
    await asyncio.sleep(n)
    print("done", n)
    return n

async def sequential():
    t0 = time.time()
    await work(2)
    await work(1)
    print("sequential took", time.time() - t0)

async def concurrent_with_gather():
    t0 = time.time()
    await asyncio.gather(work(2), work(1))
    print("gather took", time.time() - t0)

async def concurrent_with_tasks():
    t0 = time.time()
    t1 = asyncio.create_task(work(2))
    t2 = asyncio.create_task(work(1))
    await t1
    await t2
    print("tasks took", time.time() - t0)

async def main():
    await sequential()
    await concurrent_with_gather()
    await concurrent_with_tasks()

asyncio.run(main())
```

Expected approximate timings (seconds):

- sequential took ~3.0
- gather took ~2.0
- tasks took ~2.0

### Example C — run blocking code in threadpool

```py
# s1_executor.py
import asyncio, time
from concurrent.futures import ThreadPoolExecutor
import time as tm

def blocking(n):
    print("blocking start", n)
    tm.sleep(n)
    print("blocking end", n)
    return n

async def main():
    loop = asyncio.get_running_loop()
    t0 = time.time()
    # schedule blocking on default threadpool
    fut = loop.run_in_executor(None, blocking, 2)
    # while blocking runs, event loop can do other async work:
    await asyncio.sleep(0.1)
    res = await fut
    print("result", res, "took", time.time() - t0)

asyncio.run(main())
```

Expected: event loop not frozen; blocking runs in a thread.

### Example D — Semaphore concurrency limit

```py
# s1_semaphore.py
import asyncio, time

async def job(i, sem):
    async with sem:
        print("start", i)
        await asyncio.sleep(1)
        print("end", i)
        return i

async def main():
    sem = asyncio.Semaphore(2)   # allow 2 concurrent jobs
    t0 = time.time()
    results = await asyncio.gather(*(job(i, sem) for i in range(6)))
    print("results", results, "took", time.time() - t0)

asyncio.run(main())
```

Expected time: ~3 seconds (6 jobs, 2 at a time, each 1s -> ceil(6/2)=3 rounds).

### Example E — Cancellation

```py
# s1_cancel.py
import asyncio

async def worker():
    try:
        print("worker start")
        await asyncio.sleep(5)
        print("worker done")
    except asyncio.CancelledError:
        print("worker received cancel, cleaning up")
        raise

async def main():
    t = asyncio.create_task(worker())
    await asyncio.sleep(0.1)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("confirm cancel")

asyncio.run(main())
```

Expected: shows cancel flow and cleanup message.

### Example F — TaskGroup (Python 3.11+)

```py
# s1_taskgroup.py  (requires Python 3.11+)
import asyncio

async def w(n):
    await asyncio.sleep(n)
    print("done", n)
    return n

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(w(1))
        tg.create_task(w(2))
    print("TaskGroup scope ended")

asyncio.run(main())
```

TaskGroup automatically waits for children and cancels all if one fails.

---

# Short practice exercises (Stage 1) — type them & check

1. **What happens when you call, but don’t `await` a coroutine?**

   - Type `c = greet()` and `print(c)` (see Example A). Then `asyncio.run(c)`.

2. **Sequential vs concurrent timing.**

   - Run `s1_task_vs_await.py` and confirm timing numbers.

3. **Cancel a task** (see `s1_cancel.py`). Add a `finally:` block in `worker` to simulate cleanup.

4. **Concurrency limit** — change `Semaphore(2)` to `Semaphore(3)` and predict runtime.

5. **Blocking inside a coroutine** — replace `await asyncio.sleep(1)` with `time.sleep(1)` in `job()` and observe what breaks.

6. **Thread pool experiment** — in `s1_executor.py`, add another `await asyncio.sleep(0.5)` after you schedule `run_in_executor` and measure times.

Solutions: the examples above contain correct code and expected results; type them to verify.

---

# Short glossary (one-line quick cheat sheet)

- `async def`: declares a coroutine function.
- `coroutine object`: result of calling an `async def` — nothing runs yet.
- `await`: pause here; let the loop run others until result ready.
- `asyncio.create_task()`: schedule coroutine to run soon (background).
- `asyncio.gather(...)`: wait for many awaitables and collect results.
- `loop.run_in_executor(...)`: execute blocking code in a thread/process.
- `Semaphore`: limit concurrency.
- `CancelledError`: exception raised into cancelled coroutine.
- `TaskGroup`: structured concurrency (3.11+).

---

# What Stage 2 will cover (deeper technical explanations)

When you’re comfortable with the above, Stage 2 will dig deep into:

- How coroutines are implemented (state machines, frame objects, `send()`/`throw()` API).
- The internal difference between `Task` and `Future`, how results and exceptions are stored.
- Event loop internals: how it polls OS I/O, timers, and schedules callbacks (selector, epoll/kqueue).
- Cancellation propagation, `finally` and resource cleanup, and `asyncio.shield`.
- GIL internals and when the GIL matters; differences in concurrency vs parallelism at CPU level.
- Performance tips: when to use threadpool vs process pool; memory and latency tradeoffs.
- Debugging async code: tracing tasks, `PYTHONASYNCIODEBUG`, `all_tasks()`, and avoiding ephemeral background tasks.
- Structured concurrency patterns: how TaskGroup enforces lifetimes; cancellation semantics.
- JS comparison: microtask/macrotask queues vs Python microtask semantics for `await`/`.then()`.

---

# Recommended resources (start here)

- Python `asyncio` docs — tutorial & library reference: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
- PEP 492 (`async` / `await` semantics): [https://peps.python.org/pep-0492/](https://peps.python.org/pep-0492/)
- `concurrent.futures` docs (thread/process pools): [https://docs.python.org/3/library/concurrent.futures.html](https://docs.python.org/3/library/concurrent.futures.html)
- Practical walkthroughs: Real Python — Async IO in Python (search “Real Python async IO”)
- For JS async background (useful mental model): MDN docs on Promises & `async/await`.

(If you want, I’ll fetch the exact Real Python and MDN URLs and annotate which sections to read first.)

---

# Final: quick checklist before we go to Stage 2

- Did you _type and run_ at least examples A and B (coroutine vs awaited)?
- Did you run the sequential vs gather timing example? (confirm times)
- Did you try cancelling a running Task? (see `s1_cancel.py`)
- If you’re on Python < 3.11, skip TaskGroup for now — we’ll show a polyfill pattern in Stage 2.

When you say “go,” I’ll start **Stage 2** and we’ll open the hood: real internals, memory/state diagrams, how `await` becomes `yield`/`send`, how Tasks are scheduled, how the OS integrates with the loop, and advanced patterns (timeouts, retries, backpressure, TaskGroup internals).

Perfect 👍 let’s level up.
Stage 2 = **Internals & Mechanics of Python Async**.
This is where we go _under the hood_ — what actually happens when you write `async def`, `await`, or `create_task`. By the end of Stage 2 you’ll know what’s happening in memory, in the Python interpreter, and in the event loop when your coroutines run.

---

# **Stage 2 – Deep Dive into Async Internals**

We’ll cover:

1. **What exactly is a coroutine under the hood**
2. **How `await` works (state machines, yield-from)**
3. **Tasks vs Futures**
4. **Event loop internals: how it schedules coroutines**
5. **How asyncio integrates with the OS**
6. **Cancellation and exceptions**
7. **Comparisons with JavaScript promises/event loop**

Each section includes **definitions**, **illustrations**, and **small experiments**.

---

## 1. What exactly is a coroutine?

- **At runtime, an `async def` function is compiled into a _coroutine function_.**
- Calling it doesn’t execute the body immediately. Instead, it returns a **coroutine object**.
- That object implements the _generator protocol_ (`.send()`, `.throw()`, `.close()`).

👉 Coroutines are basically specialized generators that yield control back to the event loop whenever they hit `await`.

### Mini experiment

```py
import asyncio

async def demo():
    print("step 1")
    await asyncio.sleep(0.1)
    print("step 2")

coro = demo()
print(coro)                # <coroutine object demo at ...>
print(coro.__class__.__mro__)
```

You’ll see `coroutine` in the type hierarchy. This proves it’s an object, not magic.

---

## 2. How `await` works (state machines, yield-from)

When you write:

```py
await something()
```

### What happens internally

1. The coroutine suspends itself.
2. It tells the event loop: _“resume me when the thing I awaited finishes.”_
3. The event loop runs other tasks while waiting.
4. When the awaited task resolves, the event loop calls `.send(value)` on your coroutine, resuming execution right after the `await`.

### Compiler trick

Under the hood, `await` is implemented as a **`yield from`** statement. That’s why coroutines and generators share mechanics.

👉 Think of every `await` as a **checkpoint** in your coroutine’s state machine.

---

## 3. Tasks vs Futures

- **Future**: low-level object = “a box that will eventually contain a result or exception.”
  (like a promise in JS).

- **Task**: higher-level wrapper that runs a coroutine inside the event loop and produces a Future-like object.

So:

```py
task = asyncio.create_task(demo())
```

is essentially:

1. Create a Future.
2. Run your coroutine step-by-step until completion.
3. Store the result/exception inside the Future.
4. Give you back the Task object so you can `await` it.

### Mini experiment

```py
import asyncio

async def slow():
    await asyncio.sleep(1)
    return "done"

async def main():
    task = asyncio.create_task(slow())
    print("Task created:", task)
    result = await task
    print("Result:", result)

asyncio.run(main())
```

Observe the Task object printed before it finishes, then after completion.

---

## 4. Event loop internals: how it schedules coroutines

The event loop is the **orchestra conductor**:

- It maintains a queue of _ready tasks_.
- It picks the next task, runs it until it `await`s.
- Suspended tasks go back into a waiting list.
- When an awaited operation (timer, socket read, threadpool job) completes, the task is put back into the ready queue.

👉 In CPython, this is implemented in `_asyncio` C code, but the logic is:
**“Run until await → schedule next → resume when ready.”**

### Mini experiment

Trace running tasks:

```py
import asyncio

async def tick(name):
    for i in range(3):
        print(name, "step", i)
        await asyncio.sleep(0.1)

async def main():
    await asyncio.gather(tick("A"), tick("B"))

asyncio.run(main())
```

Notice how A and B interleave. That’s the loop switching between coroutines.

---

## 5. How asyncio integrates with the OS

The loop doesn’t _poll coroutines_ blindly — it asks the **operating system kernel**:

- On Linux: `epoll` / `select`
- On macOS/BSD: `kqueue`
- On Windows: IOCP

These are OS-level APIs that let the event loop wait efficiently for “file/socket ready,” “timer done,” etc.

That’s how async scales to thousands of sockets: the loop asks the OS _“tell me when any of these are ready”_, instead of blocking per connection.

---

## 6. Cancellation and exceptions

- Cancelling a Task injects a `CancelledError` into the coroutine.
- The coroutine can `try/except` it to clean up, or just let it bubble up.

### Mini experiment

```py
import asyncio

async def worker():
    try:
        print("start")
        await asyncio.sleep(2)
        print("done")
    except asyncio.CancelledError:
        print("cancelled!")
        raise

async def main():
    t = asyncio.create_task(worker())
    await asyncio.sleep(0.5)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("confirmed cancelled")

asyncio.run(main())
```

---

## 7. Comparison with JavaScript async

- **Python coroutine ↔ JS async function**
- **Python Future ↔ JS Promise**
- **`await` works the same**: pause here, resume later.
- **Event loop**: both languages use one, but JS’s loop also has the distinction between _microtasks_ (Promises) and _macrotasks_ (setTimeout). Python doesn’t split them the same way.

---

# Stage 2 Exercises

1. Write a coroutine that counts 1–5, sleeping 0.2s each time. Run 2 copies concurrently. Observe the interleaving.
2. Create a Task, then cancel it after 0.1s. Handle `CancelledError`.
3. Write a blocking `time.sleep(1)` in a coroutine and see what happens compared to `await asyncio.sleep(1)`.
4. Build your own `mini_event_loop` with just a list of coroutines and `.send(None)` until completion — see the mechanics yourself.

---

# Stage 2 Resources

- [PEP 492: Coroutines with async/await](https://peps.python.org/pep-0492/)
- [PEP 3156: Asyncio event loop](https://peps.python.org/pep-3156/)
- Python source: [`_asyncio` C implementation](https://github.com/python/cpython/tree/main/Modules/_asynciomodule.c)
- Excellent explainer: [David Beazley’s Curious Course on Coroutines](https://www.dabeaz.com/coroutines/)

---

✅ If Stage 1 gave you the **tools**, Stage 2 gives you the **X-ray vision** into how those tools work.
Stage 3 will be about **patterns and real-world design** (timeouts, retries, backpressure, queues, async streams, structured concurrency).

---

Do you want me to sketch a **mini event loop in pure Python** (Stage 2.5) so you can see how `.send()`/`await` actually schedule tasks step by step? That’s usually the “aha!” moment.

Perfect — let’s do **Stage 2.5: Practical Interaction with FastAPI Endpoints**.

This stage is all about:

- Learning to **test endpoints in different ways** (browser, `curl`, Postman).
- Practicing **GET and POST** requests.
- Seeing how to pass **query parameters, path parameters, and JSON bodies**.
- Doing this on both **Windows** and **Mac/Linux**, since the syntax can be slightly different.
- Tying it back to what you learned in Stage 2 about request/response flow.

---

# 📘 Stage 2.5: Practical Interaction with FastAPI Endpoints

---

## 1. Recap of Key Terms

Before diving in, let’s redefine some terms from Stage 1–2:

- **Endpoint**: A URL path in your app (e.g., `/hello`) that maps to a function.
- **Method (GET, POST, etc.)**: How you interact with the endpoint (read, write, update).
- **Request**: What the client sends (parameters, JSON, etc.).
- **Response**: What the server sends back (JSON, HTML, error, etc.).
- **Query parameter**: Comes after `?` in a URL (e.g., `/items?name=apple`).
- **Path parameter**: Part of the URL path itself (e.g., `/items/123`).
- **JSON body**: Data sent inside the request (mostly for POST/PUT).

---

## 2. Browser Testing (Easiest)

If you start your FastAPI app:

```bash
uvicorn main:app --reload
```

FastAPI runs at:
👉 `http://127.0.0.1:8000`

Try in your **browser**:

- `http://127.0.0.1:8000/hello` → calls a GET endpoint.
- `http://127.0.0.1:8000/items/42` → calls an endpoint with a path parameter.
- `http://127.0.0.1:8000/items?name=banana` → calls an endpoint with a query parameter.

💡 For POST requests, browsers alone won’t cut it (they default to GET), so we need `curl` or another tool.

---

## 3. Using `curl`

### 3.1. GET Requests

**Windows PowerShell**

```powershell
curl.exe http://127.0.0.1:8000/hello
```

**Mac/Linux (Terminal)**

```bash
curl http://127.0.0.1:8000/hello
```

Both should return JSON like:

```json
{ "message": "Hello World" }
```

---

### 3.2. Query Parameters

If you have:

```python
@app.get("/items")
def read_item(name: str):
    return {"item_name": name}
```

**Windows**

```powershell
curl.exe "http://127.0.0.1:8000/items?name=banana"
```

**Mac/Linux**

```bash
curl "http://127.0.0.1:8000/items?name=banana"
```

Returns:

```json
{ "item_name": "banana" }
```

---

### 3.3. Path Parameters

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**Windows**

```powershell
curl.exe http://127.0.0.1:8000/items/42
```

**Mac/Linux**

```bash
curl http://127.0.0.1:8000/items/42
```

Response:

```json
{ "item_id": 42 }
```

---

### 3.4. POST with JSON Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return {"received": item}
```

**Windows PowerShell**

```powershell
curl.exe -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d "{`"name`": `"apple`", `"price`": 1.25}"
```

**Mac/Linux**

```bash
curl -X POST http://127.0.0.1:8000/items/ -H "Content-Type: application/json" -d '{"name": "apple", "price": 1.25}'
```

Response:

```json
{ "received": { "name": "apple", "price": 1.25 } }
```

⚠️ Notice on Windows you must escape quotes differently (`\"` vs `` `" ``).

---

## 4. Swagger Docs (FastAPI Feature)

FastAPI **automatically generates interactive docs**:

- Open `http://127.0.0.1:8000/docs` → Swagger UI.
- Open `http://127.0.0.1:8000/redoc` → Alternative ReDoc UI.

👉 You can click buttons, fill forms, and try requests without `curl`.

---

## 5. Practical Exercises

1. Add a `GET /ping` endpoint that returns `{"status": "alive"}`.
2. Add a `GET /greet?name=...` endpoint that greets someone.
3. Add a `GET /math/{x}/{y}` endpoint that returns their sum.
4. Add a `POST /todo` endpoint that accepts a JSON `{task: str, done: bool}`.
5. Test all of these with:

   - Browser (for GET).
   - `curl` on Windows/Mac.
   - Swagger Docs.

---

## 6. Resources to Dig Deeper

- **FastAPI Official Docs**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **curl Cheat Sheet**: [https://curl.se/docs/httpscripting.html](https://curl.se/docs/httpscripting.html)
- **HTTP Methods Explained**: [MDN Reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

---

✅ Now you should be confident **sending real requests to your FastAPI app** and seeing how GET, POST, path parameters, query parameters, and JSON bodies differ.

---

Would you like me to follow this with **Stage 3: Concurrency in Python (async/await, ThreadPoolExecutor, create_task, gather, etc.)** — or do you want a **Stage 2.6** where we go deeper into `curl` with advanced options (headers, auth, debugging)?

Perfect — we’ll start **Stage 3: Concurrency in Python & FastAPI**, but we’ll also sprinkle in progressively **deeper `curl` usage** so you’re testing real concurrency in action. That way, you learn both the theory and the practical tools together.

---

# 📘 Stage 3: Concurrency, Async, and Threading in Python (with FastAPI)

---

## 1. Core Idea: Why Concurrency?

When a server handles requests:

- **Synchronous/blocking code** means each request must finish before the next starts.
- **Concurrent/asynchronous code** lets multiple requests overlap (useful when waiting on slow things like disk, network, or APIs).

💡 Important: **Concurrency ≠ Parallelism**.

- _Concurrency_: Tasks start, stop, and interleave (like juggling).
- _Parallelism_: Tasks truly run at the same time (multiple CPUs).

---

## 2. What is a Coroutine?

We saw this word earlier — let’s define it clearly:

- A **coroutine** is a special kind of Python function that can be paused and resumed.
- Declared with `async def`.
- They don’t run until you explicitly `await` them (or schedule them with tools like `asyncio.create_task`).

Example:

```python
import asyncio

async def say_hello():
    print("Hello ...")
    await asyncio.sleep(1)  # pause here, let others run
    print("... World!")

asyncio.run(say_hello())
```

👉 Output:

```
Hello ...
... World!
```

---

## 3. FastAPI and `async def`

FastAPI recognizes two types of endpoints:

```python
@app.get("/sync")
def sync_endpoint():
    import time
    time.sleep(3)   # blocks the whole thread
    return {"message": "Done (sync)"}

@app.get("/async")
async def async_endpoint():
    import asyncio
    await asyncio.sleep(3)  # only blocks THIS coroutine
    return {"message": "Done (async)"}
```

---

## 4. Testing Concurrency with `curl`

Let’s use `curl` to see the difference between blocking and non-blocking.

### 4.1 Sequential (One by One)

**Mac/Linux**

```bash
time curl "http://127.0.0.1:8000/sync"
time curl "http://127.0.0.1:8000/sync"
```

**Windows PowerShell**

```powershell
Measure-Command { curl.exe "http://127.0.0.1:8000/sync" }
Measure-Command { curl.exe "http://127.0.0.1:8000/sync" }
```

👉 Each call takes ~3s, so total ~6s.

---

### 4.2 Concurrent Calls (Multiple at Once)

**Mac/Linux**

```bash
time ( curl "http://127.0.0.1:8000/async" & curl "http://127.0.0.1:8000/async" )
```

**Windows PowerShell**

```powershell
Measure-Command { Start-Job { curl.exe "http://127.0.0.1:8000/async" }; Start-Job { curl.exe "http://127.0.0.1:8000/async" }; Get-Job | Wait-Job | Receive-Job }
```

👉 Both return after ~3s total, not 6s — proof of concurrency.

---

## 5. `asyncio` Tools You’ll See in FastAPI

- **`await`** → Wait for a coroutine to finish.
- **`asyncio.create_task(func())`** → Start running a coroutine _without waiting_.
- **`asyncio.gather(coro1, coro2, ...)`** → Run several coroutines concurrently, wait for all.

Example:

```python
@app.get("/tasks")
async def tasks():
    import asyncio

    async def work(n):
        await asyncio.sleep(2)
        return f"Task {n} done"

    results = await asyncio.gather(work(1), work(2), work(3))
    return {"results": results}
```

👉 Call it:

```bash
curl http://127.0.0.1:8000/tasks
```

Response after ~2s (not 6s):

```json
{ "results": ["Task 1 done", "Task 2 done", "Task 3 done"] }
```

---

## 6. Mixing in `ThreadPoolExecutor`

Not everything supports `await`. For blocking CPU or library calls, you can offload work to a thread pool:

```python
from concurrent.futures import ThreadPoolExecutor
import time, asyncio

executor = ThreadPoolExecutor()

def slow_blocking(n):
    time.sleep(3)
    return f"Blocking task {n} done"

@app.get("/threaded")
async def threaded():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, slow_blocking, 5)
    return {"result": result}
```

👉 Run and test:

```bash
curl http://127.0.0.1:8000/threaded
```

It works without blocking other async endpoints.

---

## 7. Curl Depth: Extra Options

As we progress, you can add these:

- `-v` → verbose (see headers, status, etc.)

  ```bash
  curl -v http://127.0.0.1:8000/sync
  ```

- `-w "%{time_total}\n"` → print total time

  ```bash
  curl -w "%{time_total}\n" -o /dev/null -s http://127.0.0.1:8000/async
  ```

- `--parallel` (Mac/Linux modern curl only) → built-in concurrency

  ```bash
  curl --parallel http://127.0.0.1:8000/async http://127.0.0.1:8000/async
  ```

---

## 8. Exercises

1. Create `/parallel` endpoint that runs 3 coroutines concurrently with `gather`.
2. Create `/blocking` endpoint that sleeps with `time.sleep(3)`.
3. Use `curl` to call both endpoints in parallel and compare total time.
4. Add `-v` and `-w "%{time_total}\n"` to analyze latency.

---

## 9. Resources

- [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)
- [FastAPI async docs](https://fastapi.tiangolo.com/async/)
- [curl advanced usage](https://curl.se/docs/manual.html)

---

✅ Stage 3 takeaway:

- You now understand **coroutines, async/await, gather, create_task, and ThreadPoolExecutor**.
- You can **prove concurrency** using `curl` on both Windows and Mac/Linux.
- You’ve started adding **advanced curl options** for timing and debugging.

---

Do you want me to continue into **Stage 3.5**, where we build a _mini real-world FastAPI app_ (like calling multiple fake APIs concurrently and merging results), so you can practice concurrency + curl testing with something closer to production?

This is **perfect** for turning your real FastAPI app into a living tutorial. We’ll treat this as the “case study project” that carries forward through all stages. I’ll break it down **piece by piece** in tutorial mode — explaining the **How, When, and Why**, what’s good, what needs refining, and where we can go deeper.

Let’s call this **Stage 4: Your Real App, Analyzed & Expanded.**

---

# 📘 Stage 4: Dissecting `main.py`

We’ll go through your app in **sections**. Each section will have:

1. **Direct Explanation** (what it does)
2. **Abstract Explanation** (why it exists, how it fits into FastAPI/web dev)
3. **Strengths / Improvements**
4. **Practice Exercises**

---

## 1. Imports & Setup

```python
import os
import logging
import asyncio
from pathlib import Path
from pydantic import BaseModel

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
```

### Explanation

- **`os` / `pathlib.Path`** → File system operations. (`os.listdir` lists directories, `Path.suffix` checks extensions).
- **`asyncio`** → Event loop, async tools (sleep, gather, etc).
- **`logging`** → Standard Python logging (production-grade logging system).
- **`pydantic.BaseModel`** → Used to validate request data (like JSON input in POST).
- **`fastapi.*`** → Core FastAPI tools.
- **`Jinja2Templates`** → Template rendering (dynamic HTML pages).

### Why It’s Here

- You’re combining **API backend** + **basic frontend rendering** in one project.
- Logging and Pydantic are **production best practices**.

### Strengths

✅ Correct imports, covers multiple responsibilities.
✅ Uses `pathlib` (modern, preferred over `os.path`).

### Improvements

- You use **both `os` and `pathlib`**. Consider sticking to one for consistency (prefer `pathlib`).
- Move imports into **grouped order** (standard library → 3rd party → local).

---

## 2. App Initialization

```python
VALID_EXTENSIONS = {".mcam", ".vnc"}

app = FastAPI(title="SourceRevision", version="0.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

REPO_PATH = "repo"
```

### Explanation

- **`VALID_EXTENSIONS`** → Only show files with these suffixes.
- **`FastAPI()`** → Creates the app object (router + middleware + docs engine).
- **`app.mount("/static", ...)`** → Serves static files like CSS/JS/images.
- **`templates`** → Where Jinja looks for HTML templates.
- **`REPO_PATH`** → Your "working directory" for file operations.

### Why It’s Here

- Splitting **data (repo files)** and **presentation (templates/static)** matches MVC patterns.

### Strengths

✅ `title` and `version` → auto-documentation gets metadata.
✅ Static/template setup → ready for frontend integration.

### Improvements

- `REPO_PATH` should probably come from **config/env variable** (`os.environ.get("REPO_PATH", "repo")`).
- Add **Path objects** instead of string `"repo"`.

---

## 3. Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### Explanation

- Sets up basic logging (INFO level, standard format).
- `logger = logging.getLogger(__name__)` → module-specific logger.

### Why It’s Here

Logging is vital in production: debugging, monitoring, error tracing.

### Strengths

✅ Uses logging instead of `print` (professional).

### Improvements

- Could route logs to file/rotation (via `logging.handlers`).
- FastAPI integrates with **Uvicorn logging**, so sometimes you extend instead of override.

---

## 4. Root Endpoint

```python
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

### Explanation

- **Path `/`** → Returns an HTML template.
- `request` must be passed for Jinja2 integration.

### Why It’s Here

- This is your **entry point**: homepage.
- HTML served directly from backend = good for dashboards or internal tools.

### Strengths

✅ Proper `async def`.
✅ Correct use of `TemplateResponse`.

### Improvements

- Might add **error handling** for missing `index.html`.
- Use `Path` for template existence check in development mode.

---

## 5. `/api/files` Endpoint

```python
@app.get("/api/files")
async def get_files():
    logger.info("Fetching all files")
    files_to_return = []
    try:
        repo_files = os.listdir(REPO_PATH)
        for filename in repo_files:
            if Path(filename).suffix in VALID_EXTENSIONS:
                files_to_return.append(
                    {"name": filename, "status": "available"})
    except FileNotFoundError:
        print(f"ERROR: The repository directory '{REPO_PATH}' was not found.")
        return []

    return files_to_return
```

### Explanation

- Lists files in `repo`.
- Filters by extension.
- Returns JSON of files + status.

### Why It’s Here

- This is the **core API** — lets frontend know what files exist.

### Strengths

✅ Async-friendly signature.
✅ Clear filtering logic.

### Improvements

- `os.listdir` is **blocking** → replace with `await asyncio.to_thread(os.listdir, REPO_PATH)`.
- Use `Path(REPO_PATH).iterdir()` for clarity.
- Return structured JSON (e.g., `{"files": [...]}` instead of raw list).

---

## 6. `/api/files/{filename}` Endpoint

```python
@app.get("/api/files/{filename}")
def get_file(filename: str):
    valid_files = [file for file in os.listdir(REPO_PATH)]
    if filename not in valid_files:
        raise HTTPException(404, f"File '{filename}' not found")
    return {
        "filename": filename,
        "status": "available",
        "size": "1.2 MB",
        "last_modified": "2025-10-01"
    }
```

### Explanation

- Returns metadata about a file.
- Validates existence in repo.

### Strengths

✅ Proper 404 handling with `HTTPException`.

### Improvements

- Use `Path.stat()` to get real size + last modified.
- Make function `async`.

---

## 7. `/sync-slow` vs `/async-fast`

These are **demo endpoints** — showing blocking vs non-blocking.
Perfect to test concurrency (with `curl` from Stage 3).

---

## 8. Checkout Endpoint

```python
class FileCheckout(BaseModel):
    filename: str
    user: str
    message: str

@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {
        "success": True,
        "message": f"User '{checkout.user}' checked out '{checkout.filename}'",
        "details": checkout.message
    }
```

### Explanation

- Accepts JSON body (`filename`, `user`, `message`).
- Validates with Pydantic (`BaseModel`).

### Why It’s Here

- Demonstrates **POST + validation**.
- Extensible (checkout logic, DB writes, etc).

### Strengths

✅ Clean model validation.
✅ Returns structured JSON.

### Improvements

- Make async (`async def`).
- Save checkouts somewhere (DB/file) instead of ephemeral return.

---

# ✅ Suggested Stage 4 Exercises

1. Refactor `/api/files` → use `asyncio.to_thread` and `pathlib`.
2. Enhance `/api/files/{filename}` → return real file size/modified date.
3. Add structured error logging with `logger.error()`.
4. Use `curl` (Windows/Mac) to test concurrency of `/sync-slow` vs `/async-fast`.
5. Create a **new endpoint** `/api/files/summary` that returns count by extension.

---

👉 Next Step:
Would you like me to **rewrite your code with best practices applied** (async I/O, pathlib, structured JSON, error handling), and we walk through the differences line by line in tutorial mode? That way, your `main.py` evolves into a production-grade reference.

# Refactoring tutorial (step-by-step): improve your FastAPI app without a full rewrite

Nice — we’ll **refactor your app incrementally**. For every change I’ll show **(A)** the _before_ snippet (what you have), **(B)** the _after_ snippet (the refactor), and then explain **why** the change is safer/cleaner/faster and **how** to validate it (including concrete `curl` commands for mac/linux and PowerShell). I’ll also call out trade-offs and tests to run. Do each step manually in your repo so you learn what each change does.

---

## Start: safety checklist (do this first)

1. Make a git branch: `git checkout -b refactor/step-1`
2. Run the app, confirm current behavior, and save outputs from curl (baseline).
3. Add `REPO_PATH` test folder with a couple of files (valid/invalid extensions) to test endpoints.

**Baseline curl checks**

Mac / Linux:

```bash
# homepage
curl -sS http://127.0.0.1:8000/ | head -n 5
# list files
curl -sS http://127.0.0.1:8000/api/files | jq .
# file metadata (replace FILENAME)
curl -sS http://127.0.0.1:8000/api/files/yourfile.mcam | jq .
# post checkout
curl -sS -X POST http://127.0.0.1:8000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{"filename":"yourfile.mcam","user":"you","message":"test"}' | jq .
```

Windows PowerShell:

```powershell
curl.exe http://127.0.0.1:8000/ -UseBasicParsing
curl.exe "http://127.0.0.1:8000/api/files" | ConvertFrom-Json
curl.exe "http://127.0.0.1:8000/api/files/yourfile.mcam" | ConvertFrom-Json
curl.exe -X POST http://127.0.0.1:8000/api/checkout -H "Content-Type: application/json" `
  -d '{"filename":"yourfile.mcam","user":"you","message":"test"}' | ConvertFrom-Json
```

Confirm current behavior and timings — we’ll compare after each refactor.

---

## Step 1 — Prefer `pathlib`, config from environment, and consistent filesystem handling

**Why:** `pathlib.Path` is more explicit and safer than mixing `os` and strings. Put `REPO_PATH` in config/env so it’s not hardcoded.

### (A) Before — your current lines

```py
REPO_PATH = "repo"
# later
repo_files = os.listdir(REPO_PATH)
for filename in repo_files:
    if Path(filename).suffix in VALID_EXTENSIONS:
        ...
```

### (B) After — refactor (small change)

Create a tiny `config` block at the top (or `config.py` later):

```py
from pathlib import Path
import os

# get repo path from env or default
REPO_PATH = Path(os.environ.get("REPO_PATH", "repo")).resolve()
VALID_EXTENSIONS = {".mcam", ".vnc"}
```

Use `Path` everywhere:

```py
repo_files = [p for p in REPO_PATH.iterdir() if p.suffix in VALID_EXTENSIONS and p.is_file()]
for p in repo_files:
    files_to_return.append({"name": p.name, "status": "available"})
```

**Why this is better**

- `Path.resolve()` gives absolute path and normalizes `..` (helps security later).
- `Path.iterdir()` yields `Path` objects with `.stat()`, `.name`, `.suffix`, `.exists()` — more robust and readable.

**Validation**

- Re-run baseline curl calls for `/api/files`. Output should be the same (but now fields are `p.name`).

**Trade-offs**

- Minimal. This is just clarity & correctness.

---

## Step 2 — Make filesystem operations non-blocking (use `asyncio.to_thread` or `run_in_executor`)

**Why:** `os.listdir` / `Path.iterdir()` and `Path.stat()` are blocking I/O. In async servers you must avoid blocking the event loop. Use `asyncio.to_thread()` (Py 3.9+) to run blocking calls on a thread pool.

### (A) Before — blocking `get_files`

```py
@app.get("/api/files")
async def get_files():
    logger.info("Fetching all files")
    files_to_return = []
    try:
        repo_files = os.listdir(REPO_PATH)
        for filename in repo_files:
            if Path(filename).suffix in VALID_EXTENSIONS:
                files_to_return.append({"name": filename, "status": "available"})
    ...
    return files_to_return
```

### (B) After — async-safe using `asyncio.to_thread`

```py
from typing import List
from pydantic import BaseModel

class FileInfo(BaseModel):
    name: str
    status: str

@app.get("/api/files", response_model=List[FileInfo])
async def get_files():
    logger.info("Fetching all files")

    def list_valid_files():
        if not REPO_PATH.exists():
            raise FileNotFoundError(str(REPO_PATH))
        return [p for p in REPO_PATH.iterdir() if p.is_file() and p.suffix in VALID_EXTENSIONS]

    try:
        valid_paths = await asyncio.to_thread(list_valid_files)
    except FileNotFoundError:
        logger.error("Repo path not found: %s", REPO_PATH)
        return []

    return [{"name": p.name, "status": "available"} for p in valid_paths]
```

**Why this is better**

- `asyncio.to_thread()` offloads blocking work to a thread so the event loop keeps serving other requests.
- Using `response_model` gives automatic doc generation and validation.

**If you need to support Python < 3.9**: replace `asyncio.to_thread(fn)` with:

```py
loop = asyncio.get_running_loop()
valid_paths = await loop.run_in_executor(None, list_valid_files)
```

**Validation**

- Run `/api/files` and confirm response.
- Simulate several concurrent requests (see below `curl` concurrency test) and confirm `async` endpoints stay responsive.

**Curl concurrency test** (Mac/Linux):

```bash
# many parallel calls
for i in {1..10}; do curl -sS http://127.0.0.1:8000/api/files >/dev/null & done; wait
```

PowerShell:

```powershell
1..10 | ForEach-Object { Start-Job -ScriptBlock { curl.exe http://127.0.0.1:8000/api/files | Out-Null } } | Wait-Job
```

Compare server responsiveness vs a blocking implementation.

---

## Step 3 — Secure file metadata & path traversal protection + use real metadata

**Why:** Your `get_file` currently trusts `os.listdir` and string matching. That risks _path traversal_ if a user requests `../../secrets`. Use `Path.resolve()` and ensure final path is under `REPO_PATH`.

### (A) Before — current `get_file`

```py
@app.get("/api/files/{filename}")
def get_file(filename: str):
    valid_files = [file for file in os.listdir(REPO_PATH)]
    if filename not in valid_files:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")
    return {"filename": filename, "status": "available", "size": "1.2 MB", "last_modified": "2025-10-01"}
```

### (B) After — secure, async-safe, real metadata

```py
from fastapi.responses import FileResponse
from fastapi import Path as FastAPIPath

@app.get("/api/files/{filename}", response_model=dict)
async def get_file(filename: str = FastAPIPath(..., description="Name of file in repo")):
    # Build the candidate path then resolve to prevent traversal
    candidate = (REPO_PATH / filename)
    try:
        candidate_resolved = await asyncio.to_thread(candidate.resolve)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Ensure the resolved path is inside REPO_PATH
    try:
        candidate_resolved.relative_to(REPO_PATH)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid filename (path traversal)")

    if not candidate_resolved.exists() or not candidate_resolved.is_file():
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found")

    stat = await asyncio.to_thread(candidate_resolved.stat)
    return {
        "filename": candidate_resolved.name,
        "status": "available",
        "size_bytes": stat.st_size,
        "last_modified": stat.st_mtime
    }
```

**Optional: Serve file download**

```py
@app.get("/api/files/{filename}/download")
async def download_file(filename: str):
    candidate = (REPO_PATH / filename).resolve()
    if not candidate.exists() or not candidate.is_file() or not str(candidate).startswith(str(REPO_PATH)):
        raise HTTPException(404)
    return FileResponse(path=str(candidate), filename=candidate.name)
```

**Why this is better**

- Prevents path traversal attacks.
- Returns real `stat()` data (size, mtime).
- Uses `FileResponse` for efficient file sending.

**Validation**

- Test normal metadata call:

```bash
curl -sS http://127.0.0.1:8000/api/files/yourfile.mcam | jq .
```

- Try a traversal attempt (should be blocked):

```bash
curl -sS http://127.0.0.1:8000/api/files/../main.py
# expect 400 or 404
```

---

## Step 4 — Make POST checkout persistent (and async-safe)

**Why:** Right now POST returns a message but doesn’t persist a checkout. For robustness, persist checkouts (e.g., as files in a `.checkouts` folder or a tiny SQLite DB). Use `to_thread` for filesystem writes or an async DB library for DB writes.

### (A) Before — your current `checkout_file`

```py
@app.post("/api/checkout")
def checkout_file(checkout: FileCheckout):
    return {"success": True, "message": f"User '{checkout.user}' checked out '{checkout.filename}'", ...}
```

### (B) After — persist to a simple JSON lines file (threaded)

```py
from datetime import datetime
import json

CHECKOUT_LOG = REPO_PATH / ".checkouts"
CHECKOUT_LOG.parent.mkdir(parents=True, exist_ok=True)  # ensure repo exists

async def append_checkout_record(record: dict):
    def _append():
        with open(CHECKOUT_LOG, "a", encoding="utf8") as f:
            f.write(json.dumps(record) + "\n")
    await asyncio.to_thread(_append)

@app.post("/api/checkout")
async def checkout_file(checkout: FileCheckout):
    record = {
        "filename": checkout.filename,
        "user": checkout.user,
        "message": checkout.message,
        "time": datetime.utcnow().isoformat()
    }
    await append_checkout_record(record)
    logger.info("Checkout: %s by %s", checkout.filename, checkout.user)
    return {"success": True, "record": record}
```

**Why this is better**

- Keeps a permanent audit trail (simple and easy).
- Uses filesystem writes off the event loop.
- You can later replace persistent backend with a DB without changing endpoint signature.

**Trade-offs**

- JSON-lines file is simple but limited for concurrency; if you expect heavy write load use a proper DB or queue service.

**Validation**

- POST with curl and then `tail` the `.checkouts` file to verify it was written.

---

## Step 5 — Organize code: split routers & services (project structure)

**Why:** Keep `main.py` thin and readable. Move endpoints into `routers/files.py`, models into `models.py`, and service code into `services/repo.py`. This makes testing and maintenance easier.

### Suggested structure

```
app/
  main.py        # create app, include routers, startup/shutdown
  config.py      # BaseSettings for configuration
  models.py      # Pydantic models
  routers/
    files.py     # APIRouter for file-related endpoints
  services/
    repo.py      # file system operations (sync/blocking functions called via to_thread)
  templates/
  static/
```

### (A) Before — single big `main.py` (what you have)

### (B) After — minimal `main.py` (example)

```py
# app/main.py
from fastapi import FastAPI
from .config import settings
from .routers import files

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(files.router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

And `app/routers/files.py` contains the endpoints; `app/services/repo.py` contains `list_files()`, `get_file_stat()`, `append_checkout()`. Keep service functions synchronous (blocking) but call them with `asyncio.to_thread()` inside routers — that keeps testable pure functions.

**Why this is better**

- Separation of concerns: routing vs business logic vs config.
- Easier unit testing (test `services/repo.py` directly).
- Scalability: multiple routers (auth, audit, etc) are trivial to add.

**Validation**

- Run app and test endpoints again. Nothing should break.

---

## Step 6 — Logging improvements & error handling

**Why:** Replace `print()` with `logger.*` and configure Uvicorn logging integration.

### improvements

- Replace `print(f"ERROR: ...")` with `logger.error("Repo dir not found: %s", REPO_PATH, exc_info=True)`.
- Use `logger.exception()` inside except blocks when you want stack traces.
- Add exception handlers or middleware for consistent HTTP error formatting.

**Example change**

```py
except FileNotFoundError as exc:
    logger.exception("Repository directory missing: %s", REPO_PATH)
    raise HTTPException(status_code=404, detail="Repository not found")
```

**Add request logging middleware**

```py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Start request path=%s", request.url.path)
    try:
        response = await call_next(request)
        logger.info("Completed request path=%s status=%s", request.url.path, response.status_code)
        return response
    except Exception as exc:
        logger.exception("Unhandled error for %s", request.url.path)
        raise
```

**Validation**

- Trigger an error (e.g., set `REPO_PATH` to nonexistent) and watch logs.
- Confirm you now get clearer error messages and stack traces in logs.

---

## Step 7 — Add background task / caching to improve perf

**Why:** If `repo` is expensive to list and updates infrequently, cache results in memory and refresh in the background. This avoids frequent disk roundtrips and reduces latency.

### example (simple periodic refresh)

```py
from asyncio import create_task

FILES_CACHE = []
CACHE_TTL_SECONDS = 5

async def refresh_cache_periodically():
    while True:
        try:
            FILES_CACHE[:] = await asyncio.to_thread(lambda: [p for p in REPO_PATH.iterdir() if p.is_file()])
            await asyncio.sleep(CACHE_TTL_SECONDS)
        except Exception:
            logger.exception("Cache refresh failed")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    create_task(refresh_cache_periodically())
```

**Why this is good**

- Fast responses from memory, reduced disk I/O under load.

**Caveats**

- Cache staleness vs correctness tradeoff. For real correctness use file-system event watching (e.g., `watchdog`) or background DB indexing.

**Validation**

- Request `/api/files` repeatedly and measure latency (should be lower). Then touch files and wait for TTL to expire and see changes appear.

---

## Step 8 — Tests (unit + integration)

**Why:** Prevent regressions during refactors.

### Quick unit test example with `pytest` + FastAPI `TestClient` (sync)

```py
# tests/test_files.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_files_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("REPO_PATH", str(tmp_path))
    resp = client.get("/api/files")
    assert resp.status_code == 200
    assert resp.json() == []
```

### Async integration with `httpx.AsyncClient`

```py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_files(tmp_path, monkeypatch):
    monkeypatch.setenv("REPO_PATH", str(tmp_path))
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/files")
        assert r.status_code == 200
```

**Validation**

- Add tests and run `pytest`. Fix errors exposed by refactors.

---

## Step 9 — Deployment hints

- If endpoints are mostly I/O-bound and asynchronous, run `uvicorn app.main:app --host 0.0.0.0 --port 8000` (no worker needed for concurrency).
- If you have CPU-bound load or want process isolation, use `--workers N` (each is whole process with own loop).
- Use an ingress/load-balancer in production (nginx) and enable structured logging and monitoring.

**curl concurrency test (advanced timing)**

Mac/Linux:

```bash
# measure total elapsed time for 10 concurrent requests (async endpoints)
time bash -c 'for i in {1..10}; do curl -sS http://127.0.0.1:8000/async-fast >/dev/null & done; wait'
# show per-request timings
for i in {1..5}; do curl -w "time_total=%{time_total}\n" -o /dev/null -s http://127.0.0.1:8000/async-fast; done
```

PowerShell:

```powershell
# spawn jobs
1..10 | ForEach-Object { Start-Job -ScriptBlock { curl.exe -s http://127.0.0.1:8000/async-fast | Out-Null } } | Wait-Job
# measure individually
curl.exe -w "%{time_total}\n" -o NUL -s http://127.0.0.1:8000/async-fast
```

---

## Step 10 — Checklist & next steps (pick one to implement now)

- [ ] Step 1: Replace `os.listdir` usage with `Path` + env config.
- [ ] Step 2: Offload blocking FS calls with `asyncio.to_thread`.
- [ ] Step 3: Secure path handling and return real `stat()` metadata.
- [ ] Step 4: Persist checkouts (file or DB) and make endpoint async.
- [ ] Step 5: Split routes/services into package structure.
- [ ] Step 6: Improve logging & add request-logging middleware.
- [ ] Step 7: Add cache/background refresh if listing is heavy.
- [ ] Step 8: Add tests with `pytest` and `TestClient` / `httpx.AsyncClient`.
- [ ] Step 9: Add CI checks and deploy with `uvicorn` (configure workers per workload).

---

## Quick reference: small code snippets you can copy one-by-one

**To-thread helper (compat fallback):**

```py
import asyncio
import sys

async def run_blocking(fn, *args, **kwargs):
    if sys.version_info >= (3,9):
        return await asyncio.to_thread(fn, *args, **kwargs)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))
```

**Safe resolve + check in one helper:**

```py
def is_subpath(parent: Path, child: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False
```

---

## Exercises for you (do 1–2 now)

1. Implement **Step 2** (`asyncio.to_thread` in `/api/files`) and test concurrency with the curl loops above. Report any blocking behaviors you still see.
2. Implement **Step 3** (path traversal guard) for `/api/files/{filename}` and test a malicious path like `../main.py`.
3. Move the `/api/files` endpoints into `app/routers/files.py` and include it from `main.py` (so you experience code organization).

If you want, tell me **which step you’ll do first** and I’ll give a line-by-line guided walkthrough for _only that step_ (with real diffs, exact edits, and `git` commands) so it’s painless.
