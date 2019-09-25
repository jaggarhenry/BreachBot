import discord
import requests
import time


#######################
#configuration details#
#######################

#discord bot token
TOKEN = ''

#production discord channel id
channel_id = ''









#Get breaches from last session
oldBreaches = []
oldLeaks = {}

for line in open("breaches", "r").readlines():
  line = line.replace("\n", "")

  oldBreaches.append(line)



#Make request for latest breaches
r = requests.get("https://feeds.feedburner.com/HaveIBeenPwnedLatestBreaches")



#XML to list
def parseForLatest(response):
  latestBreaches = []

  #parse as xml
  soup = BeautifulSoup(response, "xml")

  items = soup.find_all('item')

  #get names of latest breaches and add to list
  for item in items:
    latestBreaches.append(item.find_all('guid')[0].text)

  return latestBreaches





#Extract the new breaches
def checkForNewBreaches(latestBreaches):
  for line in open("breaches", "r+").readlines():
    line = line.replace("\n", "")

    oldBreaches.append(line)

  if latestBreaches != oldBreaches:
    return list(set(latestBreaches) - set(oldBreaches))





client = discord.Client()


@client.event
async def alertDiscord(breach):

    channel = client.get_channel(int(channel_id))

    embed = discord.Embed()
    embed.set_author(name="New Breach", icon_url="http://www.pngmart.com/files/8/Exclamation-Mark-Transparent-PNG.png")
    embed.add_field(name="Company:", value=str(breach), inline=True)
    await channel.send(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


    while True:
        #Reset the newBreaches or you'll be spammed. Trust me on this one.
        newBreaches = []
        oldBreaches = []

        r = requests.get("https://feeds.feedburner.com/HaveIBeenPwnedLatestBreaches")

        latestBreaches = parseForLatest(r.text)
        newBreaches = checkForNewBreaches(latestBreaches)


        #give me that sweet, sweet update email
        if newBreaches != None:
            for breach in newBreaches:
              await alertDiscord(breach)

              time.sleep(1)

            oldBreaches = latestBreaches

            #update breaches file
            with open("breaches", "w") as file:
              for breach in oldBreaches:
                file.write(breach + "\n")

        time.sleep(5)

client.run(TOKEN)