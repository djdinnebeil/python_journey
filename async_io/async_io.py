import asyncio
import time

async def task(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay} seconds")

async def main():
    start = time.time()

    # Run tasks concurrently
    await asyncio.gather(
        task("Task 1", 2),
        task("Task 2", 3),
        task("Task 3", 1)
    )

    end = time.time()
    print(f"All tasks completed in {end - start:.2f} seconds")

asyncio.run(main())