import asyncio
import requests
from aiohttp import ClientSession
import random
import string
import time

responses_to_send = 10000


class Statistics:
    def __init__(self) -> None:
        self.responses_to_send = 5
        self.processed_responses = 0
        self.unprocessed_responses = 0

    def inc_processed_responses(self):
        self.processed_responses += 1

    def inc_unprocessed_responses(self):
        self.unprocessed_responses += 1


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


async def send_test_request(session, task_num: int, s: Statistics):

    rand_name = f'{task_num}_{randomword(20)}'
    print(rand_name)

    async with session.post('http://localhost:8001/users', json={'name': rand_name}) as raw_response:
        print(raw_response.status)
        if raw_response.status == 200:
            s.inc_processed_responses()
            print('krasava', task_num)

        else:
            print('hui', task_num)
            s.inc_unprocessed_responses
        return


async def main():
    tasks = []
    s = Statistics()
    async with ClientSession() as session:
        for i in range(responses_to_send):
            task = asyncio.create_task(send_test_request(session, i, s=s))
            tasks.append(task)
        await asyncio.gather(*tasks)

    print('responses_to_send', responses_to_send)
    print('processed_responses', s.processed_responses)
    print('unprocessed_responses', s.unprocessed_responses)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    finish = time.time()
    print('work time', finish-start)
