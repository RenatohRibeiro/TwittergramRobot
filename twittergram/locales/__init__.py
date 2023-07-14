# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2021-2022 Luiz Renato (ruizlenato@protonmail.com)
import logging
import os
from functools import wraps

import yaml
from pyrogram.enums import ChatType
from pyrogram.types import CallbackQuery

from ..database.locales import get_db_lang

log = logging.getLogger(__name__)

LANGUAGES: dict[str] = {}

for file in os.listdir("twittergram/locales"):
    if file not in ("__init__.py", "__pycache__"):
        log.info("\033[90m[!] - Language %s loadded.\033[0m", file)
        with open("twittergram/locales/" + file, encoding="utf8") as f:
            content = yaml.load(f, Loader=yaml.CLoader)
            LANGUAGES[file.replace(".yaml", "")] = content


async def get_string(message, module, name):
    try:
        lang = LANGUAGES[await get_db_lang(message)]["strings"][module][name]
    except KeyError:
        lang = LANGUAGES["en_US"]["strings"][module][name]

    return lang


def locale(module):
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            if (
                message.message.chat.type
                if isinstance(message, CallbackQuery)
                else message.chat.type
            ) == ChatType.CHANNEL:
                return None
            strings = LANGUAGES[await get_db_lang(message)]["strings"][module]

            return await func(client, message, *args, strings, **kwargs)

        return wrapper

    return decorator
