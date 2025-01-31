# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2022 Hitalo M. <https://github.com/HitaloM>
# Copyright (c) 2021 Andriel <https://github.com/AndrielFR>

from time import time
from typing import Dict, Optional

from .core import database

conn = database.get_conn()


async def get_chat_by_id(id: int) -> Optional[Dict]:
    cursor = await conn.execute("SELECT * FROM chats WHERE id = ?", (id,))
    row = await cursor.fetchone()
    await cursor.close()
    return row


async def filter_chats_by_language(language: str) -> Optional[Dict]:
    cursor = await conn.execute("SELECT * FROM chats WHERE language = ?", (language,))
    row = await cursor.fetchall()
    await cursor.close()
    return row


async def register_chat_by_dict(info: Dict) -> Dict:
    id = info["id"]

    await conn.execute(
        "INSERT INTO chats (id, registration_time) VALUES (?, ?)", (id, time())
    )
    if conn.total_changes <= 0:
        raise AssertionError
    await conn.commit()

    return await get_chat_by_id(id)
