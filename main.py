import asyncio

async def main()->None:
    ... #TODO: code it
    while len(asyncio.all_tasks())>1:
        await asyncio.sleep(0.5)


asyncio.run(main())