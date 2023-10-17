import discord
from discord.ext import commands
import asyncio
import sqlite3
import datetime
import os

import queue



print("Booting up.\nDefining Token.")


if os.path.isfile("developer.txt"):
    token = ''
    print("Detected Developer mode.")
else:
    token = ''
    print("Did not detect Developer mode.")

print("Defining the Client")
client = commands.Bot(command_prefix='m!')
client.cn = False

client.loaded_exts = {
    "commands.help.help": "Help",
    "commands.load.load": "Load",
    "commands.reload.reload": "Reload",
    "commands.unload.unload": "Unload"
}
client.cmds = {}

print("Loaded module: commands.help.help")
print("Loaded module: commands.unload.unload")
print("Loaded module: commands.reload.reload")
print("Loaded module: commands.load.load")
for i in os.listdir(os.path.join(os.getcwd(), "commands")):
    if os.path.isdir(os.path.join(os.getcwd(), "commands", i)) and os.path.isfile(os.path.join(os.getcwd(), "commands",
                                                                                        i, i + ".py")):
        client.load_extension("commands." + i + "." + i)
        print("Loaded module: commands." + i + "." + i)

for i in os.listdir(os.path.join(os.getcwd(), "mechanisms")):
    if os.path.isdir(os.path.join(os.getcwd(), "mechanisms", i)) and os.path.isfile(
            os.path.join(os.getcwd(), "mechanisms",
                            i, i + ".py")):
        client.load_extension("mechanisms." + i + "." + i)
    print("Loaded module: mechanisms." + i + "." + i)


client.dev = []

client.caps = []
client.ecaps = {}
client.ocaps = {}
client.slowmode = []
client.eslowmode = {}
client.oslowmode = {}
client.invite = []
client.einvite = {}
client.blacklisted = []
client.vc = {}
client.q = {}
client.pl = {}
client.vs = {}
client.voters = {}
client.cc = {}

if os.path.isfile("blacklist.txt"):
    f = open("blacklist.txt", "r")
    client.blacklisted = [x.strip() for x in f.readlines()]
    f.close()

client.slowmode_lastmessage = {}

client.usable = []
client.mute = {}

print("Connecting to the databases.")

warndb = sqlite3.connect("warnings.db")
warncur = warndb.cursor()
sinfodb = sqlite3.connect("serverinfo.db")
sinfocur = sinfodb.cursor()
rolesdb = sqlite3.connect("roles.db")
rolescur = rolesdb.cursor()
ccdb = sqlite3.connect("cc.db")
cccur = ccdb.cursor()
sinfocur.execute("CREATE TABLE IF NOT EXISTS maxwarn (server TEXT, maxint INT)")
sinfocur.execute("CREATE TABLE IF NOT EXISTS warnexpire (server TEXT, days INT)")
sinfocur.execute("CREATE TABLE IF NOT EXISTS filter (server TEXT, ecaps TEXT, eslowmode TEXT, einvite TEXT, "
                 "caps TEXT, slowmode TEXT, invite TEXT, ocaps TEXT, oslowmode TEXT)")
sinfocur.execute("CREATE TABLE IF NOT EXISTS premium (server TEXT, start INT, expire INT)")
sinfodb.commit()
client.scheduled_warns = []

client.croles = {}
client.rids = {}

@client.event
async def on_ready():
    if client.cn is False:
        t = datetime.datetime.now() - d1
        print("Connected to Discord. (" + str(t.total_seconds()) + "s)")
        client.load_extension("CommandHandler")
        print("Loaded Command Handler.")
        d2 = datetime.datetime.now()
        client.loop.create_task(client.get_cog("PlanningSys").planning_sys())
        serversnow = list(client.servers)
        for i in serversnow:
            if i.id in client.blacklisted:
                await client.leave_server(i)
                continue

            client.croles[i.id] = {}
            client.rids[i.id] = {}
            dbserv = "server" + i.id
            rolescur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (roleid TEXT, correlationid TEXT, "
                                                                      "rid TEXT)")
            rolesdb.commit()
            sinfocur.execute("SELECT * FROM maxwarn WHERE server=?", [i.id])
            if not sinfocur.fetchall():
                sinfocur.execute("INSERT INTO maxwarn (server, maxint) VALUES (?, ?)", [i.id, 3])
                sinfodb.commit()
            sinfocur.execute("SELECT * FROM warnexpire WHERE server=?", [i.id])
            if not sinfocur.fetchall():
                sinfocur.execute("INSERT INTO warnexpire (server, days) VALUES (?, ?)", [i.id, 30])
                sinfodb.commit()
            sinfocur.execute("SELECT * FROM filter WHERE server=?", [i.id])
            if not sinfocur.fetchall():
                sinfocur.execute("INSERT INTO filter (server, ecaps, eslowmode, einvite, caps, slowmode, invite, ocaps,"
                                 " oslowmode) VALUES (?, 'none', 'none', 'none', 'false', 'false', 'false', '1', '5')",
                                 [i.id])
                sinfodb.commit()
            warncur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (timestamp TEXT, userid TEXT, expiry TEXT)")
            warndb.commit()

            client.mute[i.id] = discord.utils.get(i.role_hierarchy, name="m-mute")
            if client.mute[i.id] is not None:
                if client.mute[i.id].permissions != discord.Permissions.none():
                    await client.edit_role(i, client.mute[i.id], name="m-mute", permissions=discord.Permissions.none())
                cn = list(i.channels)
                overwrite = discord.PermissionOverwrite(send_messages=False)
                for j in cn:

                    if j.overwrites_for(client.mute[i.id]).pair() != overwrite.pair():
                        await client.edit_channel_permissions(j, client.mute[i.id], overwrite=overwrite)


            warncur.execute("SELECT rowid, * FROM " + dbserv)
            row = warncur.fetchone()
            while row is not None:
                if row[3] != "never":
                    schedule = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                    usr = await client.get_user_info(row[2])
                    await client.get_cog("WarnScheduler").warn_scheduler(i, usr, schedule, row[0])
                row = warncur.fetchone()

            sinfocur.execute("SELECT caps, slowmode, invite FROM filter WHERE server = ?", [i.id])
            mfilter = sinfocur.fetchall()[0]
            if mfilter[0] == 'true':
                client.caps.append(i.id)
            if mfilter[1] == 'true':
                client.slowmode.append(i.id)
            if mfilter[2] == 'true':
                client.invite.append(i.id)

            rolescur.execute("SELECT * FROM " + dbserv)
            row = rolescur.fetchone()
            while row:
                roleid = row[0]
                correlid = row[1]
                rid = row[2]
                if roleid not in client.croles[i.id]:
                    client.croles[i.id][roleid] = []
                if correlid:
                    client.croles[i.id][roleid].append(correlid)
                client.rids[i.id][roleid] = rid
                row = rolescur.fetchone()


            sinfocur.execute("SELECT ocaps, ecaps, oslowmode, eslowmode, einvite FROM filter WHERE server = ?", [i.id])
            mfilter = sinfocur.fetchall()[0]
            client.ocaps[i.id] = mfilter[0]
            client.ecaps[i.id] = mfilter[1]
            client.oslowmode[i.id] = mfilter[2]
            client.eslowmode[i.id] = mfilter[3]
            client.einvite[i.id] = mfilter[4]
            client.slowmode_lastmessage[i.id] = {}
            client.usable.append(i)

            cccur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (command TEXT, output TEXT)")
            ccdb.commit()

            client.cc[i] = {}

            cccur.execute("SELECT * FROM " + dbserv)
            row = cccur.fetchone()
            while row:
                client.cc[i][row[0]] = row[1]
                row = cccur.fetchone()

        client.svnum = 0
        client.loop.create_task(client.get_cog("PresenceChanger").presence_changer())
        t = datetime.datetime.now() - d2
        print("Started! (" + str(t.total_seconds()) + "s) Connected to " + str(len(client.usable)) + " servers.")
        client.cn = True
    else:
        t = datetime.datetime.now() - d1
        print("Reconnected to Discord. (" + str(t.total_seconds()) + "s)")

@client.event
async def on_channel_create(channel):
    if not channel.is_private:
        if channel.server.id in client.mute.keys() and client.mute[channel.server.id] is not None:
            overwrite = discord.PermissionOverwrite(send_messages=False)
            await client.edit_channel_permissions(channel, client.mute[channel.server.id],
                                                       overwrite=overwrite)

@client.event
async def on_voice_state_update(before, after):
    if after.server.id in client.mute:
        if client.mute[after.server.id] in after.roles:
            try:
                await client.server_voice_state(after, mute=True)
            except discord.Forbidden:
                pass
    if before.id == before.server.me.id and before.server in client.vc.keys() and not after.voice.voice_channel:
        if after.server in client.pl.keys():
            pl = client.pl[after.server]
            client.q[after.server] = queue.Queue()
            pl.stop()
    if after.server.me.voice_channel:
        humans = [x for x in after.server.me.voice.voice_channel.voice_members if not x.bot]
        if len(humans) == 0 and after.server in client.pl.keys():
            pl = client.pl[after.server]
            client.q[after.server] = queue.Queue()
            pl.stop()

@client.event
async def on_server_remove(server):
    if server in client.pl.keys():
        pl = client.pl[server]
        client.q[server] = queue.Queue()
        pl.stop()

@client.event
async def on_server_join(server):
    if server.id in client.blacklisted:
        await client.leave_server(server)
        return
    client.croles[server.id] = {}
    client.rids[server.id] = {}
    dbserv = "server" + server.id
    rolescur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (roleid TEXT, correlationid TEXT, "
                                                              "rid TEXT)")
    rolesdb.commit()
    sinfocur.execute("SELECT * FROM maxwarn WHERE server=?", [server.id])
    if not sinfocur.fetchall():
        sinfocur.execute("INSERT INTO maxwarn (server, maxint) VALUES (?, ?)", [server.id, 3])
        sinfodb.commit()
    sinfocur.execute("SELECT * FROM warnexpire WHERE server=?", [server.id])
    if not sinfocur.fetchall():
        sinfocur.execute("INSERT INTO warnexpire (server, days) VALUES (?, ?)", [server.id, 30])
        sinfodb.commit()
    sinfocur.execute("SELECT * FROM filter WHERE server=?", [server.id])
    if not sinfocur.fetchall():
        sinfocur.execute("INSERT INTO filter (server, ecaps, eslowmode, einvite, caps, slowmode, invite, ocaps,"
                         " oslowmode) VALUES (?, 'none', 'none', 'none', 'false', 'false', 'false', '1', '5')",
                         [server.id])
        sinfodb.commit()
    warncur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (timestamp TEXT, userid TEXT, expiry TEXT)")
    warndb.commit()
    rolescur.execute("SELECT * FROM " + dbserv)
    row = rolescur.fetchone()
    while row:
        roleid = row[0]
        correlid = row[1]
        rid = row[2]
        if roleid not in client.croles[server.id]:
            client.croles[server.id][roleid] = []
        if correlid:
            client.croles[server.id][roleid].append(correlid)
        client.rids[server.id][roleid] = rid
        row = rolescur.fetchone()
    try:
        client.mute[server.id] = discord.utils.get(server.role_hierarchy, name="m-mute")
        if client.mute[server.id] is None:
            client.mute[server.id] = await client.create_role(server, name="m-mute",
                                                         permissions=discord.Permissions.none())
        else:
            await client.edit_role(server, client.mute[server.id], name="m-mute",
                                   permissions=discord.Permissions.none())
        overwrite = discord.PermissionOverwrite(send_messages=False)
        channelsnow = server.channels
        for j in channelsnow:
            if j.overwrites_for(client.mute[server.id]) != overwrite:
                await client.edit_channel_permissions(j, client.mute[server.id], overwrite=overwrite)
    except discord.Forbidden:
        client.mute[server.id] = None

    sinfocur.execute("SELECT caps, slowmode, invite FROM filter WHERE server = ?", [server.id])
    mfilter = sinfocur.fetchall()[0]
    if mfilter[0] == 'true':
        client.caps.append(server.id)
    if mfilter[1] == 'true':
        client.slowmode.append(server.id)
    if mfilter[2] == 'true':
        client.invite.append(server.id)

    sinfocur.execute("SELECT ocaps, ecaps, oslowmode, eslowmode, einvite FROM filter WHERE server = ?", [server.id])
    mfilter = sinfocur.fetchall()[0]
    client.ocaps[server.id] = mfilter[0]
    client.ecaps[server.id] = mfilter[1]
    client.oslowmode[server.id] = mfilter[2]
    client.eslowmode[server.id] = mfilter[3]
    client.einvite[server.id] = mfilter[4]
    client.slowmode_lastmessage[server.id] = {}
    cccur.execute("CREATE TABLE IF NOT EXISTS " + dbserv + " (command TEXT, output TEXT)")
    ccdb.commit()

    client.cc[server] = {}
    cccur.execute("SELECT * FROM " + dbserv)
    row = cccur.fetchone()
    while row:
        client.cc[server][row[0]] = row[1]
        row = cccur.fetchone()

    client.usable.append(server)


    print("Ready to use on new server: " + server.name + "!")

@client.event
async def on_member_update(before, after):
    if after.server.id in client.mute:
        if client.mute[before.server.id] not in before.roles and client.mute[after.server.id] in after.roles:
            try:
                await client.server_voice_state(after, mute=True)
            except discord.Forbidden:
                pass
        elif client.mute[before.server.id] in before.roles and client.mute[after.server.id] not in after.roles:
            try:
                await client.server_voice_state(after, mute=False)
            except discord.Forbidden:
                pass



@client.event
async def on_message(message):
    if not message.channel.is_private and not message.author.bot and message.server in client.usable:
        # Caps Filter
        if message.server.id in client.caps and len(message.content) > 5:
            role = None
            if client.ecaps[message.server.id] != "none":
                try:
                    role = discord.utils.get(message.server.role_hierarchy, id=client.ecaps[message.server.id])
                except:
                    pass
            if role not in message.author.roles and not message.author.permissions_in(message.channel).manage_server:
                caps_amount = 0
                letter_amount = 0
                for letter in message.content:

                    if letter.isupper() and letter.isalpha():
                        caps_amount += 1
                    if letter.isalpha():
                        letter_amount += 1
                raport = 0
                try:
                    raport = caps_amount / letter_amount
                except ZeroDivisionError:
                    raport = 0

                if raport >= float(client.ocaps[message.server.id]):
                    try:
                        await client.delete_message(message)
                    except discord.Forbidden:
                        await client.send_message(message.channel, "**I would've deleted this message if I could!**")
                    return

        # Slowmode System
        if message.server.id in client.slowmode and not message.author.permissions_in(message.channel).manage_server:
            role = None
            if client.eslowmode[message.server.id] != "none":
                try:
                    role = discord.utils.get(message.server.role_hierarchy, id=client.eslowmode[message.server.id])
                except:
                    pass
            if role not in message.author.roles:
                sltime = float(client.oslowmode[message.server.id])
                if message.author.id in client.slowmode_lastmessage[message.server.id]:
                    if client.slowmode_lastmessage[message.server.id][message.author.id] \
                            + datetime.timedelta(seconds=sltime) > datetime.datetime.now():
                        try:
                            await client.delete_message(message)
                        except discord.Forbidden:
                            await client.send_message(message.channel,
                                                      "**I would've deleted this message if I could!**")
                        return
                    elif client.slowmode_lastmessage[message.server.id][message.author.id] \
                        + datetime.timedelta(seconds=sltime) <= datetime.datetime.now():
                        client.slowmode_lastmessage[message.server.id][message.author.id] = datetime.datetime.now()
                    else:
                        print("Error on Slowmode System")

                else:
                    client.slowmode_lastmessage[message.server.id][message.author.id] = datetime.datetime.now()

        # Anti-Advertising System
        if message.server.id in client.invite and not message.author.permissions_in(message.channel).manage_server and \
            'discord.gg' in message.content:
            role = None
            if client.einvite[message.server.id] != "none":
                try:
                    role = discord.utils.get(message.server.role_hierarchy, id=client.einvite[message.server.id])
                except:
                    pass
            if role not in message.author.roles:
                fornow = message.content.split(' ')
                for k in fornow:
                    if 'discord.gg' in k and '/' in k:
                        try:
                            invite = await client.get_invite(k)
                        except:
                            await client.delete_message(message)
                            return
                        if invite.server != message.server:
                            try:
                                await client.delete_message(message)
                            except discord.Forbidden:
                                await client.send_message(message.channel,
                                                          "**I would've deleted this message if I could!**")
                            return

        if message.content.startswith("m!"):
            command = message.content[2:].split(' ')
            def_comms = ["help", "load", "unload", "reload"]
            if command[0] in def_comms:
                if command[0] == "load" and message.author.id in client.dev:
                    try:

                        client.load_extension(command[1])
                        await client.send_message(message.channel, "Loaded module `" + command[1] + "`.")
                    except ModuleNotFoundError:
                        await client.send_message(message.channel, "Module `" + command[1] + "` does not exist.")
                elif command[0] == "unload" and message.author.id in client.dev:
                    try:

                        client.unload_extension(command[1])
                        if command[1] in list(client.loaded_exts.keys()):
                            client.loaded_exts.pop(command[1])
                        await client.send_message(message.channel, "Unloaded module `" + command[1] + "`.")
                    except ModuleNotFoundError:
                        await client.send_message(message.channel, "Module `" + command[1] + "` does not exist.")
                elif command[0] == "reload" and message.author.id in client.dev:
                    try:
                        client.unload_extension(command[1])
                        if command[1] in list(client.loaded_exts.keys()):
                            client.loaded_exts.pop(command[1])
                        client.load_extension(command[1])
                        await client.send_message(message.channel, "Reloaded module `" + command[1] + "`.")
                    except ModuleNotFoundError:
                        await client.send_message(message.channel, "Module `" + command[1] + "` does not exist.")
                elif command[0] == "help":
                    if len(command) == 2 and command[1] in list(client.cmds.keys()) and \
                                                            "commands." + command[1] + "." + command[1] in\
                                                            list(client.loaded_exts.keys()):
                        if client.cmds[command[1]][2] is None:
                            perms = "None"
                        else:
                            perms = client.cmds[command[1]][2]
                        helpstr = "Command: **" + command[1] + "**\nDescription: **" + client.cmds[command[1]][0] + \
                                  "**\nUsage: **" + client.cmds[command[1]][1] + \
                                  "**\nRequired Permissions: `" + perms + "`"
                        emb = discord.Embed(title="Help", description=helpstr, color=discord.Color.red())
                        try:
                            await client.send_message(message.author, embed=emb)
                            await client.send_message(message.channel, "**I've sent you a DM!**")
                        except discord.Forbidden:
                            await client.send_message(message.channel,
                                                           "**I cannot send you a DM! Please allow me to.**")
                    else:
                        helpstr = "Use m!help [command] for more details.\n\n"
                        for key, value in client.cmds.items():
                            if value[2] is None or getattr(message.author.permissions_in(message.channel), value[2]):
                                helpstr = helpstr + key + ", "
                            else:
                                helpstr = helpstr + "~~" + key + "~~, "
                        helpstr = helpstr[:-2]
                        emb = discord.Embed(title="Help", description=helpstr, color=discord.Color.red())
                        try:
                            await client.send_message(message.author, embed=emb)
                            await client.send_message(message.channel, "**I've sent you a DM!**")
                        except discord.Forbidden:
                            await client.send_message(message.channel,
                                                           "**I cannot send you a DM! Please allow me to.**")

            else:
                await client.get_cog("CommandHandler").handler(message, command)

d1 = datetime.datetime.now()

def start(client):
    while True:
        try:
            client.run(token)
        except ConnectionResetError:
            d1 = datetime.datetime.now()
            print("The connection has been reset. Attempting to reconnect...")
            continue
        break

start(client)
