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
	msg = msg[1:]
	msg = msg.split(' ')
	if(message.content[0] == prefix):
		if(msg[0] == "lang" and message.author.id == user):
			if msg[1] in lang_dict:
				language = lang_dict[msg[1]]
			else:
				language = msg[1]
			await message.channel.send("`Language set to: " + language + "`")
		# elif(msg[0] == "speed"):
		# 	speed = msg[1]
		elif(msg[0] == "volume" or msg[0] == "vol"):
			if(len(msg) != 2):
				await message.channel.send("`Volume is: " + str((vol*100)) + "%`")
				return
			vol = float(msg[1])/100
			if(vol > 1.00):
				vol = 1.0
			if(vol < 0.00):
				vol = 0.00
			vc.source.volume = vol
		elif(msg[0] == "bind"):
			user = message.mentions[0].id
			await message.channel.send("`Now bound to: " + message.mentions[0].display_name + "`")
		elif(msg[0] == "unbind"):
			user = 0
			await message.channel.send("`No longer bound.`")
	if(message.author.id == user and message.content[0] != prefix):
		speechObject = gTTS(text=message.content,lang=language, slow=False)
		speechObject.save("speech.mp3")
		# if speed != 1:
			# os.system("ffmpeg -i speech.mp3 -filter:a \"atempo=" + speed + "\" -vn speech.mp3")
		try:
			vc = await message.author.voice.channel.connect()
		except:
			await vc.move_to(message.author.voice.channel)
		vc.play(discord.FFmpegPCMAudio("speech.mp3"))
		vc.source = discord.PCMVolumeTransformer(vc.source)
		vc.source.volume = vol
		vc.resume()

client.run(token)
