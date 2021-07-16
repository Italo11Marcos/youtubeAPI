from googleapiclient.discovery import build

api_key = ""

def playlists_channel(channel_id):

    youtube = build("youtube", "v3", developerKey=api_key)

    playlists_response = youtube.playlists().list(
        part = "snippet",
        channelId = channel_id,
        maxResults = 50
    ).execute()

    playlists = []

    nextPage_token = None

    while True:
        response = youtube.playlists().list(
            part = "snippet",
            channelId = channel_id,
            maxResults = 50,
            pageToken=nextPage_token
        ).execute()

        playlists += response['items']

        nextPage_token = response.get('nestPageToken')

        if nextPage_token is None:
            break

    playlists_ids = list(map(lambda x: x['id'], playlists))
    #playlists_titles = list(map(lambda x: x['snippet']['title'], playlists))

    return playlists_ids


channel_id = "UCcF_6w2j1_jVyrvcouKB_NA"

x = playlists_channel(channel_id)

print(x)