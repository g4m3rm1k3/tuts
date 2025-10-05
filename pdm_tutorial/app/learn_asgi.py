import asyncio
import time


def synchronous_task(name, wait_time):
    print(f"Task {name}: start ({wait_time}s)")
    time.sleep(wait_time)  # Block whole thread
    print(f"Task {name}: done")


def run_synchronous_demo():
    print("Synchronous demo start")
    t0 = time.time()
    synchronous_task("A", 2)
    synchronous_task("B", 1)
    print("Total:", time.time() - t0)


if __name__ == "__main__":
    run_synchronous_demo()
