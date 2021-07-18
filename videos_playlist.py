from datetime import datetime 
import pandas as pd

from googleapiclient.discovery import build

api_key = ""

youtube = build("youtube", "v3", developerKey=api_key)

def playlists_channel(playlist_id):

    videos_playlist = []

    nextPage_token = None

    while True:
        response = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 50,
            pageToken=nextPage_token
        ).execute()

        videos_playlist += response['items']

        nextPage_token = response.get('nestPageToken')

        if nextPage_token is None:
            break

    videos_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos_playlist))    

    return videos_ids, videos_playlist


def videos_statistics(videos, videos_playlist):
    
    estatisticas = []

    for video in videos:
        response = youtube.videos().list(
            part='statistics',
            id=video
        ).execute()
        estatisticas += response['items']

    videos_title = list(map(lambda x: x['snippet']['title'], videos_playlist))
    url_thumbnails = list(map(lambda x: x['snippet']['thumbnails']['high']['url'], videos_playlist))
    published_date = list(map(lambda x: str(x['snippet']['publishedAt']), videos_playlist)) #conversion from ISO8601 date format
    video_description = list(map(lambda x: x['snippet']['description'], videos_playlist))
    videoid = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos_playlist))
    liked = list(map(lambda x: int(x['statistics']['likeCount']), estatisticas))
    disliked = list(map(lambda x: int(x['statistics']['dislikeCount']), estatisticas))
    views = list(map(lambda x: int(x['statistics']['viewCount']), estatisticas))
    comment = list(map(lambda x: int(x['statistics']['commentCount']), estatisticas))
    extraction_date = [str(datetime.now())]*len(videos)

    playlist_df = pd.DataFrame({'title':videos_title,
                                'video_id':videoid,
                                'video_description':video_description,
                                'published_date':published_date,
                                'extraction_date':extraction_date,
                                'likes':liked,
                                'dislikes':disliked,
                                'views':views,
                                'comment':comment,
                                'thumbnail': url_thumbnails}
                            )

    playlist_df.to_csv(r'', index=False)

playlist_id = "PL5TJqBvpXQv6SSsEgQrNwpOLTupXPuiMQ"

videos, videos_playlist = playlists_channel(playlist_id)

videos_statistics(videos, videos_playlist)

