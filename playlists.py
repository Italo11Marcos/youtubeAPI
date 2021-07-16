from googleapiclient.discovery import build

channel_id = "UCcF_6w2j1_jVyrvcouKB_NA"

youtube = build("youtube", "v3", developerKey = "")

playlists_response = youtube.playlists().list(
    part = "snippet",
    channelId = channel_id,
    maxResults = 50
).execute()

playlists = []

while playlists_response:

    for item in playlists_response['items']:

        id = item['id']
        title = item['snippet']['title']
        description = item['snippet']['description']

        print(id, title, description)

    # Se tiver próxima página, continua
    if 'nextPageToken' in playlists_response:
        playlists_response = youtube.playlists().list(
                part = "snippet",
                channelId = channel_id
            ).execute()
    else:
        break
