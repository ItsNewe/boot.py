# Konata, a multi purpose discord bot ( ´ ▽ ` )ﾉ

<p align="center">
  <img src="http://i0.kym-cdn.com/photos/images/newsfeed/000/790/781/293.gif" alt="Coming in your server like">
</p>

![Discord.py](https://img.shields.io/badge/library-discord.py%5Brewrite%5D-orange.svg?style=flat-square)
------------


Konata is a capable and experimental bot, started as a project for me to play around with, but that ended up becoming a general purpose bot, useful to have around and with administration capabilities.

------------

In order to operate correctly, Konata relies on a slqite database, which's schema must be as follows:

```sql

CREATE TABLE tokens(name TEXT PRIMARY KEY NOT NULL, token TEXT); --insert tokens manually

CREATE TABLE users(
	id TEXT PRIMARY KEY,
	username TEXT,
	osuname TEXT,
	creatime INTEGER
);

```


------------


Here are the current commands for it *(new commands are introduced every once in a while)*:

> The bot's prefix is `n$`

| Command | Purpose |
| ------------ | ------------ |
| `help` | Slides in your DMS to give you all the commands |
| `dog [breed] [sub-breed]` | Sends you a doggo picture  |
| `danbooru [tags]` | Fetches an image from Danbooru with the given tags. Said tags must be valid tags on the website  |
| `neko` | OwO? |
| `owo` | Wetuwns the given phwase in owospeak UwU |
| `account` | Creates a Konata account (useful only for osu atm, interesting stuff is cooking)  |
| `osu [Osu! username]` | Returns the Osu! stats for a given user. If you have an account and linked your Osu! username, returns your stats when no name is given  |
| `osulink [Osu! username]` |  Links your Osu! username to your account |
| `play [title/URL]` | Plays the given song |
| `skip` | Skips the current song (vote skipping is on the way) |
| `summon` | Brings the bot to the oice channel you're in |
| `leave` | Makes the bot disconnect from the voice channel |
| `ban [user] [reason]` | Bans the specified user with the given reason if any  |
| `kick [user] [reason]` | Same as `n$ban`, but for kicking  |
| `status` | Returns some of the bot's public stats  |
| `ping` | Gives you the bot latency  |
| `invite` | Gives you the bot's invite link  |

![Stats](https://discordbots.org/api/widget/366632492590956544.svg?usernamecolor=FFFFFF&topcolor=00a9ff&highlightcolor=FFFFFF&datacolor=00a9ff&middlecolor=00a9ff)
