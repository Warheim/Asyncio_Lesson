import asyncio
from aiohttp import ClientSession
from datetime import datetime
from more_itertools import chunked


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
        for chunk in chunked(range(1, 101), MAX_REQUESTS):
            cors = []
            for people_id in chunk:
                coro = make_request(people_id=people_id, client=session)
                cors.append(coro)
            responses = await asyncio.gather(*cors)
            print(responses)


start = datetime.now()
print(asyncio.run(main()))
print(datetime.now() - start)
