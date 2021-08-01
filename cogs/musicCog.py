import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class musicCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        #all the music related stuff
        self.is_playing = False
        # 2d array containing [song, channel]
        self.now_playing = []
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""
        self.loop = 0

     #searching the item on youtube
    def search_yt(self, item):
        #options for the format the youtube link send
        if item.startswith("https"):
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try: 
                    info = ydl.extract_info(item, download=False)['entries'][0]
                except Exception: 
                    return False
        else:
            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try: 
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
                except Exception: 
                    return False
    
        return {'source': info['formats'][0]['url'], 'title': info['title']}


    #recursive function to continue playing until is_playing is False , when its false it will returns back
    #the memory stack of the functions
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            if self.loop == 0:
                self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the url for FFmpeg library to play the music , source is from the dictionary from the youtube_dl library
            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            if self.loop == 0:
                self.music_queue.pop(0)


            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False



    # play command for the bot to play music
    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    #display queue function, maybe need to improvise this thing
    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
    #skip next song, first termiante music with stop() then call the play_next()
    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()
    
    #Create a pause function for the bot
    @commands.command(name="pause", help="Pause the current bot")
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
    #create a unpause function for the bot
    @commands.command(name ="unpause", help="Unpause the bot that is playing")
    async def unpause(self, ctx):
        if self.vc != "" and self.vc.is_paused():
            self.vc.resume()

    #create leave function for the bot to leave the channel and also reset all the queues and datas
    @commands.command(name="leave", help="Leave the voice channel")
    async def leave(self, ctx):

        if self.vc == "" or not self.vc.is_connected() or self.vc == None:
            return
        else:
            await self.vc.disconnect()
            self.vc = ""
            self.music_queue.clear()
            self.is_playing = False



    @commands.command(name="loop", help="Loop the bot")
    async def loop(self, ctx):
        if self.loop == 0:
            self.loop = 1
            await ctx.send("Looping mode is on")
        else: 
            self.loop = 0
            await ctx.send("Looping mode is off")


def setup(client):
    client.add_cog(musicCog(client))
