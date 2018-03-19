import sys, random
import traceback
import time
from socket import gethostname
from typing import Sequence, AnyStr

import requests
from depytg import types, methods, errors

HELP_TEXT = """A bot that sends the server's IP address.
Made with ❤ by @Depaulicious 🏳️‍🌈

Source code: https://github.com/Depau/IPBot-Telegram
Based on DepyTG: https://github.com/Depau/DepyTG"""

IP_TEXT = """Hostname: `{hostname}`
IP: `{ip}`"""


def send_help(token: AnyStr, msg: types.Message):
    send_msg = methods.sendMessage(msg.chat.id, HELP_TEXT)
    send_msg.reply_to_message_id = msg.message_id
    send_msg["disable_web_page_preview"] = True
    send_msg(token)


def send_ip(token: AnyStr, msg: types.Message):
    ip = requests.get('https://api.ipify.org').text
    hostname = gethostname()

    send_msg = methods.sendMessage(msg.chat.id, IP_TEXT.format(ip=ip, hostname=hostname))
    send_msg.reply_to_message_id = msg.message_id
    send_msg.parse_mode = "markdown"
    send_msg["disable_web_page_preview"] = True
    send_msg(token)


def parse_message(token: AnyStr, msg: types.Message, ids: Sequence[int]):
    if not 'text' in msg:
        return

    if msg.from_.id not in ids:
        print("Not authorized: {}".format(msg.from_))
        return

    username = methods.getMe()(token).username

    if "/help" in msg.text:
        if "group" in msg.chat.type:
            if msg.text == "/help@{}".format(username):
                send_help(token, msg)

        elif msg.text == "/help":
            send_help(token, msg)

    if "/ip" in msg.text:
        if "group" in msg.chat.type:
            if msg.text == "/ip@{}".format(username):
                send_ip(token, msg)

        elif msg.text == "/ip":
            send_ip(token, msg)


def parse_update(token: AnyStr, update: types.Update, ids: Sequence[int]) -> int:
    print(update)
    print()
    for i in ('message',):
        if i in update:
            parse_message(token, update[i], ids)
            break
    return update.update_id


def on_updates(token: AnyStr, updates: Sequence[types.Update], ids: Sequence[int]) -> int:
    max_id = 0
    for u in updates:
        try:
            upd_id = parse_update(token, u, ids)

            if upd_id > max_id:
                max_id = upd_id
        except errors.TelegramError:
            traceback.print_exc(file=sys.stderr)

    return max_id


def mainloop(token: AnyStr, ids: Sequence[int], offset: int = 0) -> int:
    updates = methods.getUpdates(offset)(token)
    return on_updates(token, updates, ids)


def main():
    token = sys.argv[1]
    tg_ids = [int(i) for i in sys.argv[2].split(",")]
    prev_offset = 0

    try:
        while True:
            prev_offset = mainloop(token, tg_ids, prev_offset) + 1
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
