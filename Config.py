from os import environ

def env(name: str):
    return environ[name]

class Config:
   API_ID = env(API_ID)
   API_HASH = env(API_HASH)
   BOT_TOKEN = env(BOT_TOKEN)
   DOWNLOAD_LOCATION = "./downloads/"
