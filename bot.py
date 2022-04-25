import os

import discord
import nest_asyncio
import aiohttp
nest_asyncio.apply()
from logic import fetch_cards


client = discord.Client()


@client.event
async def on_ready():
    print('{0.user} ready to fetch!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response = fetch_cards(message.content)
    for card in response['cards']:
        print('card: ', card)
        if card['fetch_type'] == 'text':
            for item in card['items']:
                await message.channel.send(item)
        elif card['fetch_type'] == 'image':
            if card['len'] == 1:
                await message.channel.send(card['items'])
            elif card['len'] > 1:
                for item in card['items']:
                    await message.channel.send(item)

client.run(os.getenv("TOKEN"))
