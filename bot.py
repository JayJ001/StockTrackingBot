import discord
import responses
import database
import schedule
import time
import asyncio
import threading
from dotenv import load_dotenv
import os

load_dotenv()

async def send_message(message, user_message, is_private):
    try: 
        if(user_message[:6] == 'Update'):
            await message.channel.send(user_message)
        else:
            response = responses.handle_response(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # for debugging
        print(f"{username} said: '{user_message}' in {channel}")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        elif user_message[0] == '!':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)

def update():
    schedule.every().day.at("16:45").do(database.updateStocks)
    schedule.every().day.at("20:13").do(database.updateStocks)
    while True:
        schedule.run_pending()
        time.sleep(1)

discord_thread = threading.Thread(target=run_discord_bot)
discord_thread.start()

update()