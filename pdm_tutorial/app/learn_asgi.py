"""
Understanding ASGI (Asynchronous Server Gateway Interface)
and the 'async' and 'await' keywords in Python.
"""
import asyncio
import time

# ============================================================================
# CONCEPT 1: Synchronous Code (The "Old Way" - WSGI)
# ============================================================================


def synchronous_task(name, wait_time):
    """A task that blocks everything while it runs."""
    import time
    print(f"Task '{name}': Starting, will take {wait_time}s.")
    time.sleep(wait_time)  # This is a blocking call. Nothing else can happen.
    print(f"Task '{name}': Finished.")


def run_synchronous_demo():
    print("\n--- Running Synchronous Demo (like WSGI) ---")
    start_time = time.time()
    synchronous_task("A", 2)  # Runs and finishes completely...
    synchronous_task("B", 1)  # ...before this one can even start.
    duration = time.time() - start_time
    print(f"Total time: {duration:.2f}s (Expected: 2 + 1 = 3s)")

# ============================================================================
# CONCEPT 2: Asynchronous Code (The "New Way" - ASGI)
# ============================================================================


async def asynchronous_task(name, wait_time):
    """
    An 'async' function is a coroutine. It can be paused and resumed.
    'await' is the pause point. It says "this might take a while,
    so let the event loop run other tasks in the meantime."
    """
    print(f"Task '{name}': Starting, will take {wait_time}s.")
    await asyncio.sleep(wait_time)  # This is a NON-blocking call.
    print(f"Task '{name}': Finished.")


async def run_asynchronous_demo():
    print("\n--- Running Asynchronous Demo (like ASGI) ---")
    start_time = time.time()
    # asyncio.gather runs multiple coroutines concurrently.
    await asyncio.gather(
        asynchronous_task("C", 2),
        asynchronous_task("D", 1)
    )
    duration = time.time() - start_time
    # The total time is determined by the LONGEST task, not the sum.
    print(f"Total time: {duration:.2f}s (Expected: max(2, 1) = 2s)")

# ============================================================================
# CONCEPT 3: When to Use `async/await`
# ============================================================================
"""
Rule of Thumb: Use `async/await` for I/O-bound operations.
- I/O-bound: Waiting for something external (network, database, file system). Your CPU is idle.
- CPU-bound: Heavy computation (math, complex loops). Your CPU is busy.

GOOD uses for async/await (I/O-bound):
- `await db.fetch_data()`   # Waiting for a database
- `await client.get(...)`   # Waiting for another API
- `await file.read()`       # Waiting for the hard drive

BAD uses for async/await (CPU-bound):
- `result = heavy_math_calculation()` # This blocks anyway, async provides no benefit.
  For CPU-bound tasks in FastAPI, you run them in a separate thread pool.
"""

if __name__ == "__main__":
    run_synchronous_demo()

    # To run async code, you need an event loop.
    asyncio.run(run_asynchronous_demo())
