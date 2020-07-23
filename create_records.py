#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:56:18 2020

@author: maxwell
"""

from youtube_transcript_api import YouTubeTranscriptApi
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

#Test video IDs. These will need to be updated with video IDs from a search script
biden_new=['i5S1jqeQOaU']
trump_new=['jDaEM46_twk','mXD4zPY4Ai0']

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console() #still working on how to bypass OAUTH2
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_trump = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=trump_new
    )
    response_trump = request_trump.execute()
    
    #add candidate and captions
    for i in range(len(trump_new)):
        response_trump['items'][i]['candidate'] = 'trump'
        response_trump['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(trump_new[i])
        
    request_biden = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=biden_new
    )
    response_biden = request_biden.execute()
    
    for i in range(len(biden_new)):
        response_biden['items'][i]['candidate'] = 'biden'
        response_biden['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(biden_new[i])

if __name__ == "__main__":
    main()
    