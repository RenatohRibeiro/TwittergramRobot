# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2021-2022 Luiz Renato (ruizlenato@protonmail.com)
from ..database import database

from pyrogram.enums import ChatType

conn = database.get_conn()


async def get_db_lang(id: int, type: str):
    if type == ChatType.PRIVATE:
        cursor = await conn.execute("SELECT lang FROM users WHERE id = (?)", (id,))
    elif type in (ChatType.GROUP, ChatType.SUPERGROUP):
        cursor = await conn.execute("SELECT lang FROM groups WHERE id = (?)", (id,))
    try:
        row = await cursor.fetchone()
        await cursor.close()
        return row[0]
    except TypeError:
        return "en-US"


async def set_db_lang(id: int, code: str, type: str):
    if type == ChatType.PRIVATE:
        await conn.execute("UPDATE users SET lang = ? WHERE id = ?", (code, id))
    elif type in (ChatType.GROUP, ChatType.SUPERGROUP):
        await conn.execute("UPDATE groups SET lang = ? WHERE id = ?", (code, id))
    await conn.commit()
