import discord
import requests
from bs4 import BeautifulSoup

# added json for reading config.json
from json import loads



class Bot(discord.Client):
    async def on_ready(self):
        # this honestly is not the best approach, but i have yet to find a better one...
        # `on_ready` should not really be used like `__init__`
        self.config = getConfig()
        print(f'We have logged in as {self.user.name}')

    async def on_message(self, message):
        # ignoring messages from self or other bots
        if message.author.bot:
            return

        if message.content.startswith('!hackernews'):
            news_embed = await fetch_hacker_news()

            # Moved the sending into `on_message` for name clarity `fetch_...` should not perform sending
            # further improvement would be to write methods in a seperate file, and as the scope increases
            # a command parser may be necesarry
            channel = self.get_channel(self.config["news-channel"])
            await channel.send(embed=news_embed)

# In testing i was unable to get any news, maybe needs fixing?
async def fetch_hacker_news() -> discord.Embed:
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.select('.storylink')

    news_embed = discord.Embed(title='Latest News from The Hacker News', color=discord.Color.blue())
    for item in news_items[:5]:
        title = item.get_text()
        link = item['href']
        news_embed.add_field(name=title, value=f'[Read more]({link})', inline=False)
    
    return news_embed


def getConfig() -> dict:
    try:
        with open("config.json", 'r') as f:
            configData = loads(f.read())

    except FileNotFoundError:
        print("Could not find file config.json")
        exit()

    except PermissionError:
        print("Could not read file config.json (Permissions missing?)")
        exit()

    else:
        return configData


# added main and run condition
def main():
    # intents should be specified
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    client = Bot(intents=intents)
    client.run(getConfig()["token"])

# in case something wants to import from this file
if __name__ == "__main__":
    main()
