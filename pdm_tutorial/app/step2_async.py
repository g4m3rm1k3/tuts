import asyncio
import time


async def asynchronous_task(name, wait_time):
    print(f"Task {name}: start ({wait_time}s)")
    # Non-blocking: yeilds control to event loop
    await asyncio.sleep(wait_time)
    print(f"Task {name}: done")


async def run_asynchronous_demo():
    print("Asynchronous demo start")
    t0 = time.time()
    await asyncio.gather(
        asynchronous_task("C", 2),
        asynchronous_task("D", 1),
    )
    print("Total:", time.time() - t0)


if __name__ == "__main__":
    asyncio.run(run_asynchronous_demo())
