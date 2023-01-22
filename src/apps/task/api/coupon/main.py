import asyncio
import random
from typing import List

import aiohttp


async def make_random_username() -> List[dict]:
    """
    유저 네임 랜덤 생성하는 함수
    """
    user_list: List[dict] = []
    cnt = 0
    while True:
        if len(user_list) >= 10:
            break
        cnt += 1
        rand_username = "user_"
        _number = str(random.randint(1, 1000))
        rand_username += _number

        if rand_username in user_list:
            continue

        user_list.append({
            'name': f'{rand_username}',
            }
        )

    # print("*****************쿠폰 구매 요청 유저 순서*****************")
    # print(user_list)
    return user_list


async def call_async_api(session, username):
    """
    쿠폰 랜덤으로 부여하는 API 호출하는 함수
    """
    data = {'username': username}
    async with session.post(
        url="http://127.0.0.1:8000/api/coupon", json=data) as response:
        res = await response.json()

        return res


async def call_api(username):
    data = {'username': username}
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://127.0.0.1:8000/api/coupon', json=data) as res:
            result = await res.json()

    return result


async def main():
    username_list = await make_random_username()
    coros = [call_api(info['name']) for info in username_list]
    res_list = await asyncio.gather(*coros)

    user_rank = []
    for res in res_list:
        for info in username_list:
            if res['username'] == info['name']:
                info['성공여부'] = res['is_success']
                info['쿠폰번호'] = res['coupon_number']
                info['rank'] = res['rank']

    for info in username_list:
        print(info)


if __name__ == "__main__":
    asyncio.run(main())
