# Telegram-Chat-Bot

A simple bot used in my personal telegram conversations. Allows users to do the following commands:

/all - tag everyone in the chat - Currently this is hardcoded per bot, since I cant find a way for a bot to look up users in a chat <br>
/cs or /play - tags people who play cs (counterstrike) \* <br>
/zias /abdullahs /ahmads /bhattis - tags people in a family \*\* <br>
/urban {{term}} - displays the definition of term from urban dictionary <br>
/wolf {{expression}} - evaluates and displays expression <br>
/help - lists commands available <br>
/test - returns a test message <br>

\* - only applies to friends bot <br>
\*\* - only applies to cousins bot

### Usage
-Change cousinsApiKeyTemplate or friendsApiKeyTemplate to cousinsApiKey.py or friendsApiKey.py and enter your telegram bot API (from bot father) there. <br>
-Run `pip install requirements` <br>
-Run python friends-telegram-bot.py or cousins-telegram-bot.py
