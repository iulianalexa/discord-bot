import datetime
import asyncio
import sqlite3

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()

class PlanningSys():
    comm = False
    def __init__(self, bot):
        self.client = bot

    async def planning_sys(self):
        while True:
            for i in self.client.scheduled_warns:
                if i[2] + datetime.timedelta(minutes=5) < datetime.datetime.now():
                    timethen = i[2] + datetime.timedelta(minutes=5)
                    delta = timethen - datetime.datetime.now()
                    delta = delta.total_seconds()
                    self.client.scheduled_warns.remove(i)
                    self.client.loop.call_later(delta, lambda: asyncio.ensure_future(self.client.emechs['unwarn_sys']
                                                                                     [1].unwarn_sys(i[0], i[1], i[3],
                                                                                                    warndb, warncur)))

            await asyncio.sleep(300)


def setup(bot):
    bot.add_cog(PlanningSys(bot))
    bot.loaded_exts['mechanisms.planning_sys.planning_sys'] = 'PlanningSys'
