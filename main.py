import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all())

files = os.listdir('C:/Users/shamil/Desktop/devtbot/commands')
for file in files:
    if file.endswith('.py'):
        bot.load_extension(f'commands.{file[:-3]}')
        


bot.run(os.getenv('TOKEN'))