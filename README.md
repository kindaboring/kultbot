# KultBot 
### The Official Discord Bot for Kult Village.

## Functionalities:

1. Upon joining, a new user will receive a direct message containing a captcha code for verification.
2. If the captcha is successful, the user will be granted access to the server through an assigned role ("villagers").
   - A log is created in the "kultbot-logs" channel for reporting features, including the user's name and Discord ID.
4. Prevents profanity, spam, nudity, and other inappropriate messages in text channels.
5. (WIP) Utilizes the Spotify API to update the Music Promotion channel with the latest released songs from assigned artists.
6. (WIP) Utilizes Instagram to update the Visual Production Photo channel with the latest Instagram posts from assigned artists.
7. (WIP) Utilizes YouTube to update the Visual Production Videos channel with the latest YouTube videos from assigned artists.

## Requirements:
- [Augmentor](https://augmentor.readthedocs.io/en/stable/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [numpy](https://numpy.org/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [nudepy](https://pypi.org/project/nudepy/)
