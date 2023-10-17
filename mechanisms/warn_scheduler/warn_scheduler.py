import datetime
import asyncio
import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class WarnScheduler():
    comm = False
    def __init__(self, bot):
        self.client = bot

    async def warn_scheduler(self, server, target, expiry, warnid):
        if expiry + datetime.timedelta(minutes=5) < datetime.datetime.now():
            timethen = expiry + datetime.timedelta(minutes=5)
            delta = timethen - datetime.datetime.now()
            delta = delta.total_seconds()
            self.client.loop.call_later(delta, lambda: asyncio.ensure_future(
                self.client.get_cog("UnwarnSys").unwarn_sys(server, target, warnid)))
        else:
            self.client.scheduled_warns.append([server, target, expiry, warnid])


def setup(bot):
    bot.add_cog(WarnScheduler(bot))
    bot.loaded_exts['mechanisms.warn_scheduler.warn_scheduler'] = 'WarnScheduler'
