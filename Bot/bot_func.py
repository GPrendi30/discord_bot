import os
import requests
import json
import random
import time
from discord.ext.commands import Bot

class Bot_func(Bot):
    
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
        
        
    def get_dad_joke(self, msg):
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
            'x-rapidapi-key': "5d7e9863f4mshc2307ea4ac84250p111d6cjsn1760d7946486",
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
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


