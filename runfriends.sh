#!/bin/bash
until python3 friends-telegram-bot.py; do
    echo "'friends-telegram-bot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
