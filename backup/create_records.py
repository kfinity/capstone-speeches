#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:56:18 2020

@author: maxwell
"""

from youtube_transcript_api import YouTubeTranscriptApi
import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from youtube_search import bidenID, trumpID
import json

#Read in existing JSON, or create if JSON does not exist
if os.path.isfile("speeches.json"):
    speeches=json.load(open('speeches.json'))
else:
    speeches=[]

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

#Read in video IDs from youtube_search.py
biden_new=[bidenID]
trump_new=[trumpID]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
service_account_file = 'service_account.json'

    # Get credentials and create an API client
credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

if trump_new == [None]:
    pass
else:
    #Get metadata
    request_trump = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=trump_new
        )
    response_trump = request_trump.execute()
        
    #add candidate and captions
    for i in range(len(trump_new)):
        response_trump['items'][i]['candidate'] = 'trump'
        response_trump['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(trump_new[i])
        
    #add to json
    speeches.append(response_trump)

if biden_new == [None]:
    pass
else: 
    #Get metadata       
    request_biden = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=biden_new
        )
    response_biden = request_biden.execute()
        
    #add candidate and captions
    for i in range(len(biden_new)):
        response_biden['items'][i]['candidate'] = 'biden'
        response_biden['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(biden_new[i])
    
    #add to json
    speeches.append(response_biden)

#write JSON file
with open('speeches.json', 'w') as outfile:
     json.dump(speeches, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)