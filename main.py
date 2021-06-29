import discord
import os
import json
import datetime 
import requests # simple and elegant Http library 
import random # importing random module 
from replit import db # importing db from replit 
import warnings
warnings.filterwarnings("ignore");

y = datetime.datetime.now()
x=print(y.strftime("%Y-%m-%d"))
client = discord.Client()



sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]

starter_encouragements = ["Cheer up!",
"Hang in there",
"You are a great a bot/person",
"Hang in there and stay positive ","You're capable ","Be positive and Stay Calm"]

if "responding" not in db.keys():
  db["responding"]=True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q'] + "-" + json_data[0]['a']
  return(quote)

def get_joke():
  url = 'https://api.jokes.one/jod?category=knock-knock'
  api_token = "YOUR API KEY HERE"
  headers = {'content-type': 'application/json',
	   'X-JokesOne-Api-Secret': format(api_token)}
  response = requests.get(url, headers=headers)
  #print(response)
  #print(response.text)
  jokes=response.json()['contents']['jokes'][0]
  return(jokes);

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]= encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragement(index):
  encouragements=db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"]=encouragements;


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return 
  msg = message.content  
 
  if msg.startswith("$RanNo"):
    await message.channel.send(random.randint(1,10000000000000000))
    

  if msg.startswith('$Covid'):
    await message.channel.send("Any questions  you have ")
    await message.channel.send('You can check the link - https://www.mohfw.gov.in/pdf/FAQ.pdf')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if msg.startswith('!fun'):
    joke = get_joke()
    await message.channel.send(joke)

  if msg.startswith('@Covax'):
    await message.channel.send("You can get the facts about covid vaccine")
    await message.channel.send("Here is the link for it - https://www.google.com/url?q=https://www.google.com/search%3Fq%3Dcovid%2Bvaccine&source=hpp&id=19024278&ct=3&usg=AFQjCNFfpRf5vuZhhcAyUcINtS4NUUU6kA&prid=243")

  if db["responding"]:
    options = starter_encouragements; 

  if "encouragements" in db.keys():
    options=starter_encouragements;
    options = options + db["encouragements"]; 

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))  

  if msg.startswith('@Bye'):
    await message.channel.send('Bye ! Hope you enjoyed this session Unitl then bye From Bot ')

  if msg.startswith('#hello'):
    await message.channel.send('Hi  welcome to the Bot!') 

  if msg.startswith('$GM'):
    await message.channel.send('Good Morning {0.user} !'.format(client)) 

  

  if msg.startswith("$new"):
    encouraging_message=msg.split("$new",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")


  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith('$list'):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"];
    await message.channel.send(encouragements)


  if msg.startswith("$responding"):
    value=msg.split("$responding",1)[1];

    if value.lower()=="true":
      db["responding"]=True;
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")    


client.run(os.getenv('TOKEN'))   