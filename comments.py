from googleapiclient.discovery import build
import pandas as pd

api_key = ''

def video_comments(video_id):
	
	#lista vazia para armazenar os comentários
	comments = []

	# lista vazia para armazenar as replies
	replies = []

	# creating youtube resource object
	youtube = build('youtube', 'v3',
					developerKey=api_key)

	# retrieve youtube video results
	video_response=youtube.commentThreads().list(
	part='snippet,replies',
	videoId=video_id
	).execute()

	while video_response:
		
		for item in video_response['items']:
			
			# Extrai os comments
			comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
			
			#total de reply do comment
			replycount = item['snippet']['totalReplyCount']

			if replycount>0:
				
				# itera por todos os comentários
				for reply in item['replies']['comments']:
					
					# Extrai comentário
					reply = reply['snippet']['textDisplay']
					
					# Adiciona o reply na lista
					replies.append(reply)

			#Print comment com seus replies
			#print(comment, replies, end = '\n\n')

			comments.append(comment)
			for reply in replies:
				comments.append(reply)

			# esvazia a lista replies
			replies = []

		# Se tiver próxima página, continua
		if 'nextPageToken' in video_response:
			video_response = youtube.commentThreads().list(
					part = 'snippet,replies',
					videoId = video_id
				).execute()
		else:
			break

	df = pd.DataFrame(comments, columns=['comentários'])

	df.to_csv(r'/home/shaka/python/api/youtubeapi/comments.csv', index=False)

# Enter video id
video_id = "eUHqqflaAJo"

# Call function
video_comments(video_id)

#### playlist from channel
#https://stackoverflow.com/questions/62347194/youtube-api-get-all-playlist-id-from-a-channel-python
#https://github.com/programacaodinamica/mini-projetos/blob/master/src/Extracao_de_dados_Youtube_Data_API_v3.ipynb
"""
import googleapiclient.discovery

channel_id = "UC1udnO-W6gpR9qzleJ5SDKw"

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "YOUR_API_KEY")

request = youtube.playlists().list(
    part = "snippet",
    channelId = channel_id,
    maxResults = 50
)
response = request.execute()

playlists = []
while request is not None:
    response = request.execute()
    playlists += response["items"]
    request = youtube.playlists().list_next(request, response)

print(f"total: {len(playlists)}")
print(playlists)
"""