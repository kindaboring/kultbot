#instagram.py
import os
import json
import requests
import traceback
from Tools.utils import getConfig, updateConfig, getGuildPrefix
from discord.ext import commands

INSTAGRAM_USERNAME = os.getenv('IG_USERNAME')
INSTAGRAM_USERNAME2 = os.getenv('IG_USERNAME2')
INSTAGRAM_USERNAME3 = os.getenv('IG_USERNAME3')

# ------------------------ COGS ------------------------ #  

class InstagramCog(commands.Cog, name="instagram"):
    def __init__(self, bot):
        self.bot = bot

@commands.Cog.listener()

# ------------------------------------------------------ #  

async def get_user_fullname(html):
    return html.json()["graphql"]["user"]["full_name"]


def get_total_photos(html):
    return int(html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html):
    return html.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def get_user_fullname(html2):
    return html2.json()["graphql"]["user"]["full_name"]


def get_total_photos(html2):
    return int(html2.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["count"])


def get_last_publication_url(html2):
    return html2.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"]


def get_last_photo_url(html2):
    return html2.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["display_url"]


def get_last_thumb_url(html2):
    return html2.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["thumbnail_src"]


def get_description_photo(html2):
    return html2.json()["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]


def webhook(webhook_url, html):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "New Instagram post from @"+INSTAGRAM_USERNAME+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    # embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url": get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))


def webhook2(webhook_url, html2):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "New Instagram post from @"+INSTAGRAM_USERNAME2+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html2)+"/"
    embed["description"] = get_description_photo(html2)
    # embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url": get_last_thumb_url(html2)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))

def webhook3(webhook_url, html):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data = {}
    data["embeds"] = []
    embed = {}
    embed["color"] = 15467852
    embed["title"] = "New Instagram post from @"+INSTAGRAM_USERNAME3+""
    embed["url"] = "https://www.instagram.com/p/" + \
        get_last_publication_url(html)+"/"
    embed["description"] = get_description_photo(html)
    # embed["image"] = {"url":get_last_thumb_url(html)} # unmark to post bigger image
    embed["thumbnail"] = {"url": get_last_thumb_url(html)}
    data["embeds"].append(embed)
    result = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json"})
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Image successfully posted in Discord, code {}.".format(
            result.status_code))

def get_instagram_html(INSTAGRAM_USERNAME):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME + "/feed/?__a=1", headers=headers)
    return html

def get_instagram2_html(INSTAGRAM_USERNAME2):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html2 = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME2 + "/feed/?__a=1", headers=headers)
    return html2

def get_instagram3_html(INSTAGRAM_USERNAME3):
    headers = {
        "Host": "www.instagram.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    html3 = requests.get("https://www.instagram.com/" + INSTAGRAM_USERNAME3 + "/feed/?__a=1", headers=headers)
    return html3

def main_instagram():
    try:
        html = get_instagram_html(INSTAGRAM_USERNAME)
        html2 = get_instagram2_html(INSTAGRAM_USERNAME2)
        html3 = get_instagram3_html(INSTAGRAM_USERNAME3)

        if(os.environ.get("LAST_IMAGE_ID") == get_last_publication_url(html)): # if the last_image_id equals the latest publication, do nothing.
            pass
        else:
            os.environ["LAST_IMAGE_ID"] = get_last_publication_url(html) # sets the last_image_id variable to the latest publication, then posts to discord.
            print("New image to post in discord.")
            webhook(os.getenv("WEBHOOK_URL"),
                    get_instagram_html(INSTAGRAM_USERNAME))
        
        #if(os.environ.get("LAST_IMAGE_ID2") == get_last_publication_url(html2)): # if the last_image_id equals the latest publication, do nothing.
        #    pass
        #else:
        #    os.environ["LAST_IMAGE_ID2"] = get_last_publication_url(html2) # sets the last_image_id variable to the latest publication, then posts to discord.
        #    print("New image to post in discord.")
        #    webhook2(os.getenv("WEBHOOK_URL"),
        #            get_instagram2_html(INSTAGRAM_USERNAME2))
        
        #if(os.environ.get("LAST_IMAGE_ID3") == get_last_publication_url(html3)): # if the last_image_id equals the latest publication, do nothing.
        #    pass
        #else:
        #    os.environ["LAST_IMAGE_ID3"] = get_last_publication_url(html3) # sets the last_image_id variable to the latest publication, then posts to discord.
        #    print("New image to post in discord.")
        #    webhook3(os.getenv("WEBHOOK_URL"),
        #            get_instagram3_html(INSTAGRAM_USERNAME3))
    
    except Exception as e:
        traceback.print_exc()
# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(InstagramCog(bot))