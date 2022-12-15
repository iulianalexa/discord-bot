#!./.venv/bin/python
import discord      # base discord module
import code         # code.interact
import os           # environment variables
import inspect      # call stack inspection
import random       # dumb random number generator

from discord.ext import commands    # Bot class and utils

################################################################################
############################### HELPER FUNCTIONS ###############################
################################################################################

# log_msg - fancy print
#   @msg   : string to print
#   @level : log level from {'debug', 'info', 'warning', 'error'}

def log_msg(msg: str, level: str):
    # user selectable display config (prompt symbol, color)
    dsp_sel = {
        'debug'   : ('\033[34m', '-'),
        'info'    : ('\033[32m', '*'),
        'warning' : ('\033[33m', '?'),
        'error'   : ('\033[31m', '!'),
    }
    # internal ansi codes
    _extra_ansi = {
        'critical' : '\033[35m',
        'bold'     : '\033[1m',
        'unbold'   : '\033[2m',
        'clear'    : '\033[0m',
    }
    # get information about call site
    caller = inspect.stack()[1]
    # input sanity check
    if level not in dsp_sel:
        print('%s%s[@] %s:%d %sBad log level: "%s"%s' % \
            (_extra_ansi['critical'], _extra_ansi['bold'],
             caller.function, caller.lineno,
             _extra_ansi['unbold'], level, _extra_ansi['clear']))
        return
    # print the damn message already
    print('%s%s[%s] %s:%d %s%s%s' % \
        (_extra_ansi['bold'], *dsp_sel[level],
         caller.function, caller.lineno,
         _extra_ansi['unbold'], msg, _extra_ansi['clear']))

################################################################################
############################## BOT IMPLEMENTATION ##############################
################################################################################

# bot instantiation
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(command_prefix='!', intents=intents)

music_root = "music" + os.path.sep
songs = {
	"craciun_disstrus": music_root + "craciun_disstrus.mp3"
}

voice_clients = {}

# on_ready - called after connection to server is established
@bot.event
async def on_ready():
    log_msg('logged on as <%s>' % bot.user, 'info')

# on_message - called when a new message is posted to the server
#   @msg : discord.message.Message
@bot.event
async def on_message(msg):
    # filter out our own messages
    #if msg.author == bot.user:
    #    return
    log_msg('message from <%s>: "%s"' % (msg.author, msg.content), 'debug')
    # overriding the default on_message handler blocks commands from executing
    # manually call the bot's command processor on given message
    await bot.process_application_commands(msg)
    
@bot.event
async def on_voice_state_update(member, before, after):
	if member.guild in voice_clients and len(voice_clients[member.guild].channel.members) == 1:
		# everyone left
		if voice_clients[member.guild].is_playing:
			voice_clients[member.guild].stop()
		await voice_clients[member.guild].disconnect()
		voice_clients.pop(member.guild)

# roll - rng chat command
#   @ctx     : command invocation context
#   @max_val : upper bound for number generation (must be at least 1)
@bot.command(brief='Generate random number between 1 and <arg>')
async def roll(ctx, max_val: int):
    # argument sanity check
    if max_val < 1:
        raise Exception('argument <max_val> must be at least 1')
    await ctx.send_response(random.randint(1, max_val))

@bot.command(brief="List all available songs")
async def list(ctx):
	message = "These are all the available songs:\n```\n"
	for song in songs:
		message = message + "%s @ %s\n" % (song, songs[song],)
	message = message + '```'
	await ctx.send_response(message)

@bot.command(brief="Disconnect from the voice channel")
async def scram(ctx):
	if ctx.guild in voice_clients:
		if voice_clients[ctx.guild].is_playing:
			voice_clients[ctx.guild].stop()
		await voice_clients[ctx.guild].disconnect()
		voice_clients.pop(ctx.guild)
		await ctx.send_response("disconnected")
	else:
		await ctx.send_response("not connected to any voice channel!")
		
@bot.command(brief="Play a song")
async def play(ctx, song):
	if song not in songs:
		await ctx.send_response("This song is not available. Use the list command.")
		return
	
	if ctx.guild in voice_clients:
		await ctx.send_response("Already connected to a voice channel!")
		return
		
	if ctx.author.voice is None:
		await ctx.send_response("You are not connected to a channel!")
		return
		
	voice_channel = ctx.author.voice.channel
	vclient = await voice_channel.connect()
	voice_clients[ctx.guild] = vclient
	vclient.play(discord.FFmpegPCMAudio(songs[song]))
	
	await ctx.send_response("playing %s" % song)
	

# roll_error - error handler for the <roll> command
#   @ctx     : command that crashed invocation context
#   @error   : ...
@roll.error
async def roll_error(ctx, error):
    await ctx.send(str(error))

################################################################################
############################# PROGRAM ENTRY POINT ##############################
################################################################################
if __name__ == '__main__':
    # check that token exists in environment
    if 'BOT_TOKEN' not in os.environ:
        log_msg('save your token in the BOT_TOKEN env variable!', 'error')
        exit(-1)
    # launch bot (blocking operation)
    bot.run(os.environ['BOT_TOKEN'])
    

