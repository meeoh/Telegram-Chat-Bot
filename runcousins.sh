#!/bin/bash
until python cousins-telegram-bot.py; do
    echo "'cousins-telegram-bot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
