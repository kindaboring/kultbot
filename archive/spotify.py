#spotify.py
import os
import json
import spotipy
import spotipy.util as util
from datetime import timedelta, date
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8b9b4fcdf7ec45a38c29cb2effd785d2",
                                                           client_secret="452efcf2f51a4a04a23efc5f04824bc5"))

async def read_app_info():
    """
        Reads from the app_info.txt file and creates a list of variables to be used by other functions.
        :return: list of variables from app_info.txt
    """
    # get info from app_info.txt
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_info.txt") # adds the path up to the file for running different working directory settings
    with open(file_name) as app_info_fp:
        client_id = app_info_fp.readline().strip()
        client_secret = app_info_fp.readline().strip()
        redirect_uri = app_info_fp.readline().strip()
        sender_email = app_info_fp.readline().strip()
        sender_password = app_info_fp.readline().strip()

    return [client_id, client_secret, redirect_uri, sender_email, sender_password]

async def check_for_dir(name):
    """ Creates the given name as a directory if it does not exist, expects a '/' at the end of the name """
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), name)): # cache_files folder does not exist
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), name))

async def set_credentials(username, client_id, client_secret, redirect_uri):
    """
        Sets the developer credentials for accessing the Spotify API and creates a Spotipy object for calling it.
        :param username: a Spotify username
        :param client_id: Spotify app client_id from app_info.txt
        :param client_secret: Spotify app client_secret from app_info.txt
        :param redirect_uri: Spotify app redirect_uri from app_info.txt
        :return: sp (a Spotipy object)
    """
    scope = "playlist-modify-private playlist-modify-public user-follow-read ugc-image-upload"

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_files/.cache-" + username) # look in cache_files
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri, path)
    sp = spotipy.Spotify(token)
    return sp

async def get_followed_artists(username, sp):
    """
        Calls the API for the user and gets a dictionary of information about the artists they follow, then turns it into a dict of artist_id:artist_name.
        :param username: a Spotify username
        :param sp: a Spotipy object
        :return: followed_artists (a dict representing information about the artists the username follows)
    """
    num_recieved_artists = 50
    after_id = None # after_id is the last artist ID retrieved from the previous request, starts as None

    followed_artists = {} # will represent information about the user's followed artists
    while num_recieved_artists == 50: # the last call to the API will get 50 or less artists
        artists_dict = sp.current_user_followed_artists(50, after_id) # call API to get a dictionary of 50 followed artists
        
        after_id = artists_dict["artists"]["cursors"]["after"] # update after_id for use in next call if necessary
        num_recieved_artists = len(artists_dict["artists"]["items"])

        for artist in artists_dict["artists"]["items"]: # populate followed_artists
            followed_artists[artist["id"]] = artist["name"]

        if after_id is None: # edge case for if user is following a number of artists divisible by 50
            break

    return followed_artists

async def update_user_info(username, sp):
    """
        Will create user_info.txt if it does not exist then fetches data from the api for each user placed in the cache_files folder.
        If a user does not exist in user_info.txt for a cache file, a playlist will be made for the user and the function will request an email via the console.
        If a user already exists in user_info.txt, their followed artists will be updated.
        :param username: a Spotify username
        :param sp: a Spotipy object
        :return: user_info (the contents of user_info.txt, a dict of information about each user)
    """
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_info.txt")
    try:
        in_file = open(file_name) # will try to open file
        user_info = json.load(in_file)
    except: # file not created yet
        user_info = {}

    if username not in user_info.keys():
        user_info[username] = {}

    # update followed_artists for the user
    user_info[username]["followed_artists"] = get_followed_artists(username, sp) # gets a dict of form artist_id:artist_name

    try: # will close the file if it was opened previously
        in_file.close()
    except:
        pass

    with open(file_name, 'w') as out_file: # write to user_info.txt, create file if it does not exist
        json.dump(user_info, out_file)

    return user_info


async def get_new_music(user_info):
    """
        Calls the API for every unique artist followed by the whole userbase.
        Gets each artist's last 5 albums and singles, determines if they are new by comparing today's date and the release date.
        If new music is found, the api data gets added to the new_music dict
        Creates the log_information dict with usernames to be filled with data later
        :param user_info: the json curently stored in user_info.txt, guaranteed up-to-date (dict)
        :param return: new_music (a dict of new music from artists the userbase follows, formatted artist_id:album_dict)
        :param return: log_information (a dict of information to later write into the logs folder, this funciton only fills it with usernames from user_info)
    """
    print("Calling API for new music")
    log_information = {}
    new_music = {}

    followed_artists = set()
    for username in user_info.keys(): # fill followed_artists with ids of all followed artists for all users, ignore duplicaates
        followed_artists.update(user_info[username]["followed_artists"].keys())
        log_information[username] = []

    for artist_id in followed_artists:
        # call api for each artist and get their last 5 albums and singles
        albums = sp.artist_albums(artist_id, "album", country="US", limit=5)
        singles = sp.artist_albums(artist_id, "single", country="US", limit=5)

        # fill a list with all the music received for the artist
        music = []
        music.extend(albums["items"])
        music.extend(singles["items"])

        for album in music:
            # get the release date and turn it into a date type
            date_parts = album["release_date"].split('-') # usually formatted: "XXXX-XX-XX"
            try:
                release_date = date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
            except:
                # the format of the release_date is not always year-month-day
                # the release_date_precision for albums can vary, for example, it may only include the year
                # in this case we ignore the release, assuming all newer music has the necessary metadata
                continue

            # this is what determines if an album is new or not
            if release_date + timedelta(days = 1) >= date.today(): # was released today or yesterday
                # if it was released yesterday, we need to make sure it was after the script ran (checks logs to do this)

                check_for_dir("logs/")

                file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/" + str(date.today() - timedelta(days = 1)) + ".txt")
                try: # see if there was a log generated yesterday
                    in_file = open(file_name) # will try to open file
                    yesterday_log = json.load(in_file)

                    #TODO this is inefficient, could be improved (also running for removed?)
                    for user in yesterday_log.keys(): # loop over each user, see if the album id was added for any of them
                        if album["id"] in yesterday_log[user]: # album has already been added to users who follow the artist
                            raise Exception("Album already added")

                    # the release has not been previously added. Add the artist if necessary, then the album
                    if artist_id in new_music.keys():
                        new_music[artist_id].append(album)
                    else:
                        new_music[artist_id] = [album]
                except:
                    # album was added yesterday, or no log could be found
                    pass

    return new_music, log_information


async def remove_users(users, user_info):
    """
        Removes users who have been previously saved in user_info.txt, but no longer appear in cache_files to prevent unnecessary API calls when getting new music.
        :param users: usernames that appear in the cache_files folder (list)
        :param user_info: the json curently stored in user_info.txt, guaranteed up-to-date (dict)
    """
    removed_user = False
    for indexed_user in list(user_info.keys())[:]:
        if indexed_user not in users:
            user_info.pop(indexed_user, None)
            removed_user = True

    if removed_user: # a user was removed from user_info, update the user_info.txt text file
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_info.txt")
        with open(file_name, 'w') as out_file:
            json.dump(user_info, out_file)

async def generate_logs(log_information):
    """ Write log_information as a json to a new dated text file in the logs folder """
    check_for_dir("logs/")

    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/" + str(date.today()) + ".txt")
    with open(file_name, 'w') as out_file: # write to user_info
        json.dump(log_information, out_file)

async def main_spotify():
    app_info = read_app_info() # get information from app_info.txt
    # app_info is formatted: [client_id, client_secret, redirect_uri, sender_email, sender_password]

    user_info = {}
    spotipy_objects = {} # to be a dict formatted as username:spotipy_object
    users = [] # will be a list of usernames from the cache_files folder

    check_for_dir("cache_files/")

    for cache_name in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_files/")): # for cache file in the cache_files folder
        username = cache_name[7:].strip() # all cache files are formatted ".cache-username"

        sp = set_credentials(username, app_info[0], app_info[1], app_info[2]) # create spotipy object and set credentials
        spotipy_objects[username] = sp
        user_info = update_user_info(username, sp)
        users.append(username)
   
        remove_users(users, user_info) # remove users who are no longer in cache_files to prevent unnecessary API calls
        new_music, log_information = get_new_music(user_info) # collect new music from artists the userbase as a whole follows