import discord
import os
import requests
import json
import random
import time

from Bot.read_token import read_api_key
from discord import File
from Brain.brain import Brain
from discord.ext.commands import Bot


class Bot(Bot):
    
    def __init__(self, name):
        self.name = name
        self.brain = Brain()
        self.joke = False
        self.id = 'DISCORD_API_KEY'
        time.sleep(2)
        
        super().__init__(command_prefix="")
    
    def run(self):
        super().run(self.id, reconnect=True)
    
    async def on_ready(self):
        print('We have logged in as {}'.format(self.user))
    
    async def on_message(self, message):
        if message.author == self.user or self.joke:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello! ' + message.author.display_name)

        elif message.content.startswith('Say something good'):
            await message.channel.send(self.get_quote())

        elif message.content.startswith('Tell me a joke'):
            question, punchline = self.get_dad_joke(message)
            
            await message.channel.send(question)
            self.set_joke(True)
            
            time.sleep(5)
            
            await message.channel.send(punchline)
            self.set_joke(False)
            
        elif message.content.startswith('Send a meme'):
            await message.channel.send(self.get_meme())
            
        elif message.content.startswith('What is your name?'):
            await message.channel.send("I am Prophet")

        elif message.content.startswith('$voice on'):
            await message.channel.send('Voice Mode activated')
            self.brain.voiceModeOn()

        elif message.content.startswith('$voice off'):
            await message.channel.send('Voice Mode deactivated')
            self.brain.voiceModeOff()

        elif message.content.startswith('$flush memory'):
            self.reset_mem(str(message.channel.id))
            await message.channel.send('I am brand new')
            
        elif message.content.startswith('$Prophetize'):
            await message.channel.send("I am a prophet")
            
        else:
            self.brain.feed(str(message.channel.id), message.content)
            answer = self.brain.answer(str(message.channel.id))
            if self.brain.hasVoice:
                await message.channel.send(file=File(answer))
            else:
                await message.channel.send(answer)
    
    def set_joke(self, mode):
        self.joke = mode


    def get_quote(self):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -- " + json_data[0]['a']
        return quote

    def get_meme(self):
        response = requests.get("https://api.imgflip.com/get_memes")
        json_data = json.loads(response.text)
        memes = json_data['data']['memes']
        
        urls = []
        
        for m in memes:
            url = m['url']
            urls.append(url)
            
        return urls[random.randint(0, len(urls) - 1)]
        
    def reset_mem(self, channel):
        self.brain.reset_memory(channel)
        
        
    def get_dad_joke(self, message):
        msg = message.content.split()
        if "about" in msg:
            term = msg[-1]
        else:
            term = ""
        
        if term == "":
            url = "https://dad-jokes.p.rapidapi.com/random/joke"
        else:
            url = "https://dad-jokes.p.rapidapi.com/joke/search?term={}".format(term)

        headers = {
            'x-rapidapi-key': "API_KEY",
            'x-rapidapi-host': "API_URL"
            }

        response = requests.request("GET", url, headers=headers)
        
        json_data = json.loads(response.text)
        jokes = []
        for j in json_data['body']:
            question = j['setup']
            punchline = j['punchline']
            jokes.append([question, punchline])
        
        joke = jokes[random.randint(0, len(jokes) - 1)]
        
        return joke[0], joke[1]