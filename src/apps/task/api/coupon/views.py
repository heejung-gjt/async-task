from datetime import datetime

import string_utils
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.common.core.redis_config import redis_config
from src.common.db.connect import connection, transaction

router = APIRouter()


import logging

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('/var/log/async')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




async def run(self, data):
    async with transaction() as session:
        sql_str = (
            f"select total from tbl_user_total FOR UPDATE of tbl_user_total"
        )
        res = await session.fetch(sql_str)
        if res[0]['total'] <= 0:
            sql_str = (
                "INSERT INTO user_info "
                "(username, coupon_number, create_at, is_success, status, user_cnt)"
                f"VALUES('{data.username}', null, '{datetime.now()}', false, 'Normal', {user_cnt})"
            )
            await session.fetch(sql_str)
            return False

        sql_str = (
            f"update tbl_user_total set total = {res[0]['total'] - 1} "
        )

        res = await session.fetch(sql_str)
        # print(res)
        user_cnt += 1
        coupon_str = await _get_random_coupon_number(session)
        sql_str = (
            "INSERT INTO user_info "
            "(username, coupon_number, create_at, is_success, status, user_cnt)"
            f"VALUES('{data.username}', '{coupon_str}', '{datetime.now()}', true, 'Normal', {user_cnt})"
        )
        await session.fetch(sql_str)


class UserInfoReq(BaseModel):
    username: str

# work = Work()

def _get_random_coupon_str() -> str:
    rand_str = string_utils.shuffle(
        "1234567890abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+="
    )
    return rand_str[:16]

async def _get_random_coupon_number(rd):
    async with connection() as session:
        while True:
            coupon_str = _get_random_coupon_str()
            sql_str = (
                f"SELECT COUNT(1) AS count FROM user_info WHERE coupon_number = '{coupon_str}'"
            )
            res = await session.fetch(sql_str)

            if res[0]['count'] <= 0:
                break

        return coupon_str

async def _save_coupon_info(username, coupon):
    async with connection() as session:
        sql_str = (
            "INSERT INTO user_info "
            "(username, coupon_number, create_at, is_success, status, user_cnt)"
            f"VALUES('{username}', '{coupon}', '{datetime.now()}', true, 'Normal', 0)"
        )
        await session.fetch(sql_str)


@router.post(
    "",
    tags=["랜덤 쿠폰"],
    name="쿠폰 랜덤 부여",
    description="",
)
async def get_random_coupon(data: UserInfoReq):
    rd = redis_config()
    rd.put(data.username)
    size = rd.size()
    if rd.size() >= 5:
        is_success = "Fail"
        coupon_number = "쿠폰 소진"
        username = data.username
    else:
        # rd.put(data.username)
        coupon_number = await _get_random_coupon_number(rd)
        await _save_coupon_info(data.username, coupon_number)
        is_success = "Success"
        username = data.username

    logger.info(f"username: {data.username}, queue_size: {rd.size}")


    return JSONResponse(
        {
        "username": username,
        "is_success": is_success,
        "coupon_number": coupon_number,
        "rank": size
        }
    )
