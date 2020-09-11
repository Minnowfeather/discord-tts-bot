# bot.py

import discord
from gtts import gTTS
import os

tokenReader = open("token.txt", "r")
token = tokenReader.read()

vc = None
vol = 100
speed = 1.0
user = 0
prefix = "<"
language = "en"
lang_dict = {
    "english":"en",
    "spanish":"es",
    "brazillian":"pt-BR",
    "japanese":"ja",
    "australian":"en-AU",
    "england":"en-GB",
    "korean":"ko",
    "indian":"en-IN"
}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global vc, vol, prefix, language, speed, user
    if message.author == client.user:
        return

    msg = message.content
    is_command = msg[:len(prefix)] == prefix
    msg = msg[len(prefix):]
    msg = msg.split(' ')
    
    if is_command:
        if is_command and msg[0] == "lang" and message.author.id == user:
            l = await set_lang(msg[1])
            if l:
                await message.channel.send("`Language set to: " + language + "`")
            else:
                await message.channel.send("`Not a valid language.`")
    
        elif msg[0] == "volume" or msg[0] == "vol":
            if(len(msg) != 2):
                await message.channel.send("`Volume is: " + str((vol*100)) + "%`")
                return
            vol = clamp(float(msg[1]) / 100, 0, 1)
            vc.source.volume = vol
                
        elif msg[0] == "bind" and user == 0:
            user = message.mentions[0].id
            await message.channel.send("`Now bound to: " + message.mentions[0].display_name + "`")
            
        elif msg[0] == "unbind" and message.author.id == user:
            user = 0
            await message.channel.send("`No longer bound.`")

    elif message.author.id == user:
        await connect(message.author.voice.channel)
        await speak(message.content)


async def connect(channel):
    global vc, vol, prefix, language, speed
    
    try:
        vc = await channel.connect()
    except:
        await vc.move_to(channel)
    
    
async def speak(message):
    global vc, vol, prefix, language, speed

    speechObject = gTTS(text = message, lang = language, slow=False)
    speechObject.save("speech.mp3")
  
    vc.play(discord.FFmpegPCMAudio("speech.mp3"))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = vol
    vc.resume()


async def set_lang(lang):
    global language
    
    prev_lang = language
    if lang in lang_dict:
        language = lang_dict[lang]
    else:
        language = lang
    
    try:
        gTTS(text = "a", lang = language, slow=False)
    except:
        language = prev_lang
        return False
    
    return True
    
 
def clamp(num, mi, ma):
    return max(min(num, ma), mi)
        

client.run(token)
