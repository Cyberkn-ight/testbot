import discord
import requests
from bs4 import BeautifulSoup

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'  # Replace with your bot token
CHANNEL_ID = 1234567890  # Replace with the ID of the channel to send the news

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.content.startswith('!hackernews'):
        await fetch_hacker_news()

async def fetch_hacker_news():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.select('.storylink')

    news_embed = discord.Embed(title='Latest News from The Hacker News', color=discord.Color.blue())
    for item in news_items[:5]:
        title = item.get_text()
        link = item['href']
        news_embed.add_field(name=title, value=f'[Read more]({link})', inline=False)

    channel = client.get_channel(CHANNEL_ID)
    await channel.send(embed=news_embed)

client.run(TOKEN)
