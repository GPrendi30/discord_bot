import os

def read_api_key():
    api_key = ""
    with open('API_TOKEN', 'r') as f:
        
        for fx in f:
            api_key += fx
            
        api_key = api_key[9:len(api_key) - 1]
        
    return api_key
