import asyncio
from aiohttp import ClientSession
from more_itertools import chunked
from db import Session, People, Base, engine


async def paste_to_db(people_list):
    async with Session() as session:
        people_list = [People(json=item) for item in people_list]
        session.add_all(people_list)
        await session.commit()


async def make_request(people_id: int, client: ClientSession):
    url = f'https://swapi.dev/api/people/{people_id}'
    client = ClientSession()
    response = await client.get(url)
    json_data = await response.json()
    await client.close()
    return json_data


MAX_REQUESTS = 10


async def main():
    async with ClientSession() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        for chunk in chunked(range(1, 101), MAX_REQUESTS):
            cors = []
            for people_id in chunk:
                coro = make_request(people_id=people_id, client=session)
                cors.append(coro)
            people_list = await asyncio.gather(*cors)
            await paste_to_db(people_list)


asyncio.run(main())
