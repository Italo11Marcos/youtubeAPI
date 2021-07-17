from googleapiclient.discovery import build
import pandas as pd

api_key = ''

def video_comments(video_id):
	
	comments = []
	replies = []

	youtube = build('youtube', 'v3', developerKey=api_key)

	video_response=youtube.commentThreads().list(
	part='snippet,replies',
	videoId=video_id
	).execute()

	while video_response:
		
		for item in video_response['items']:
			
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			
			replycount = item['snippet']['totalReplyCount']

			if replycount>0:
				for reply in item['replies']['comments']:
					reply = reply['snippet']['textDisplay']
					replies.append(reply)

			#print(comment, replies, end = '\n\n')

			comments.append(comment)
			for reply in replies:
				comments.append(reply)

			replies = []

		if 'nextPageToken' in video_response:
			video_response = youtube.commentThreads().list(
					part = 'snippet,replies',
					videoId = video_id
				).execute()
		else:
			break

	df = pd.DataFrame(comments, columns=['comentários'])

	df.to_csv(r'', index=False)

video_id = "eUHqqflaAJo"


video_comments(video_id)
