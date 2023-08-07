from bot.tg.client import TgClient

cl = TgClient()
# print(cl.get_updates(offset=0, timeout=60))
print(cl.send_message(123820005, "hellow"))