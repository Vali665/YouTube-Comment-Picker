import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Set up the YouTube API credentials
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_local_server(port=0)

# Create a YouTube API client instance
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Get the comments from a YouTube video
video_id = "VIDEO_ID"
comments = []
next_page_token = None
while True:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        # Check if the comment is between two numbers
        numbers = [int(s) for s in comment.split() if s.isdigit()]
        if len(numbers) == 2:
            num1, num2 = numbers
            if num1 < num2:
                if num1 < 0 and num2 > 0:
                    comments.append(comment)
            else:
                if num2 < 0 and num1 > 0:
                    comments.append(comment)
    
    # Check if there are more comments to retrieve
    if "nextPageToken" in response:
        next_page_token = response["nextPageToken"]
    else:
        break

# Print the comments between two numbers
for comment in comments:
    print(comment)
