
# Copyright (C) 2015 Leandro Toledo de Souza <leandrotoeldodesouza@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].


import logging
import telegram
import requests
import urbandict
from bs4 import BeautifulSoup
from time import sleep
import re
#from friendsApiKey import API_KEY, RAP_GENIUS
from friendsApiKey import *

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2


def main():

    # Telegram Bot Authorization Token
    bot = telegram.Bot(API_KEY)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            update_id = echo(bot, update_id)
        except telegram.TelegramError as e:
            # These are network problems with Telegram.
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                # The user has removed or blocked the bot.
                update_id += 1
            else:
                raise e
        except URLError as e:
            # These are network problems on our end.
            sleep(1)


def echo(bot, update_id):

    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
	#print update.message
	#print update.message.chat_id
        update_id = update.update_id + 1
	try:
	    chat_id = update.message.chat_id
	except:
	    return update_id

        try:
            # UCS-4
            patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
            # UCS-2
            patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        message = patt.sub('_emoji_', update.message.text)


        if message:
            # Reply to the message
            words = message.split(' ')
            requester = update.message.from_user.username
            with open("friendsTrainingData.txt", "a") as myfile:
                myfile.write(""" '{{"input": "{}", "output": {{ "{}": 1 }} }}'\n""".format(message, requester))
            users = "@bmann2 @meeoh @HonkeyGuy @gurmL @Newgz @KingOfTheJews @akhan47 @Braybowler"
            gamePlayers = "@bmann2 @meeoh @HonkeyGuy @Newgz @Braybowler"
            words[0] = words[0].lower()
            if (words[0] == "/all"):
                if(len(words) >= 2):
                    response = users + " " + message.split(' ', 1)[1]
                    bot.sendMessage(chat_id=chat_id, text=response)
                else:
                    bot.sendMessage(chat_id=chat_id, text=users)
            elif (words[0] == "/play"):
                if(len(words) >= 2):
                    response = gamePlayers + " " + message.split(' ', 1)[1]
                    bot.sendMessage(chat_id=chat_id, text=response)
                else:
                    bot.sendMessage(chat_id=chat_id, text=gamePlayers)
            elif (words[0] == "/urban"):
                if(len(words) < 2):
                    response = "Please provide a term to look up in the Urban Dictionary"
                    bot.sendMessage(chat_id=chat_id, text=response)
                else:
                    query = message.split(' ', 1)[1]
                    urban = urbandict.define(query)[0]
                    defn = urban["def"]
                    reply = urban["word"].rstrip() + ": " + defn + \
                        "\nexamples: " + urban["example"]
                    bot.sendMessage(chat_id=chat_id, text=reply)

            elif (words[0] == "/wolf"):
                if(len(words) < 2):
                    err = "Please provide an argument to Wolfram Alpha"
                    bot.sendMessage(chat_id=chat_id, text=err)
                else:
                    query = message.split(' ', 1)[1]
                    query = query.replace('+', 'plus')
                    r = requests.get(
                        "http://api.wolframalpha.com/v2/query?appid=E533KV-9URK4TXPJK&input=" + query + "&format=plaintext")
                    soup = BeautifulSoup(r.content, "html.parser")
                    try:
                        pod_value = soup.find_all('pod')[1].find(
                            'plaintext').contents[0]
                    except:
                        pod_value = "Invalid query for wolframalpha, try again"
                    bot.sendMessage(chat_id=chat_id, text=pod_value)

            elif (words[0] == "/help"):
                response = "The commands you can type are: \n1. '/all {{message}}' to send a message with everyone mentioned\n2. '/play {message}' to send a message with people who play games mentioned\n3. '/urban {{term}}' to define a term in urban dictionary\n 4. '/wolf {{expression}}' to evaluate an expression using wolframalpha\n 5. '/song {{query}}' to find the top 3 songs in rap genius for your query.\n"
                bot.sendMessage(chat_id=chat_id, text=response)
            elif (words[0] == "/test"):
                response = "Test message for @" + str(requester)

                bot.sendMessage(chat_id=chat_id, text=response)
            elif (words[0] == "/newgz"):
                response = ""
                for i in range(0, 100):
                    response = response + "@newgz "
                    if i == 50:
                        response = response + "\n"
                bot.sendMessage(chat_id=chat_id, text=response)
            elif (words[0] == "/song"):
                response = ""
		if(len(message.split(' ')) < 2):
			bot.sendMessage(chat_id=chat_id, text="Try /song {{lyric/artist}}")
			return update_id
                query = message.split(' ', 1)[1]
                query = query.replace(' ', '%20')
                r = requests.get("http://api.genius.com/search?q=" + query, headers = {'Authorization': 'Bearer ' + RAP_GENIUS}).json()
                for i in range(3):
                     if(r['response'] and r['response']['hits'] and r['response']['hits'][i]):
                        #pp.pprint(r['response']['hits'][i]['result']['full_title'])
                        response = response + str(i+1) + ". " + r['response']['hits'][i]['result']['full_title'] + "\n"
                if response == "":
                    response = "Couldnt find anything on rap genius"
                bot.sendMessage(chat_id=chat_id, text=response)
            elif (words[0] == "/id"):
                bot.sendMessage(chat_id=chat_id, text="ID: " + str(chat_id))

            #else:
                #response = words[0].strip(
                #) + " is not a recognized command, ask shameel to make it or stop trying dumb crap"
                #bot.sendMessage(chat_id=chat_id, text=response)

    return update_id


if __name__ == '__main__':
    main()
