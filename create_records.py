#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:56:18 2020

@author: maxwell
"""

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from youtube_search import bidenID, trumpID, harrisID, penceID
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
harris_new=[harrisID]
pence_new=[penceID]

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

#TRUMP
if trump_new == [None]:
    pass
else:
    #Get metadata
    request_trump = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=trump_new
        )
    response_trump = request_trump.execute()
    print("Ran Trump request - 1 unit")
        
    #add candidate and captions
    for i in range(len(trump_new)):
        try:
            response_trump['items'][i]['candidate'] = 'trump'
            response_trump['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(trump_new[i])
        except TranscriptsDisabled:
            print("Transcripts disabled for video: %s" % trump_new[i])
        except NoTranscriptFound:
            print("No transcript found for video: %s" % trump_new[i])
        except VideoUnavailable:
            print("Video no longer available: %s" % trump_new[i])
        
    #add to json
    speeches.append(response_trump)

#BIDEN
if biden_new == [None]:
    pass
else: 
    #Get metadata       
    request_biden = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=biden_new
        )
    response_biden = request_biden.execute()
    print("Ran Biden request - 1 unit")
        
    #add candidate and captions
    for i in range(len(biden_new)):
        try:
            response_biden['items'][i]['candidate'] = 'biden'
            response_biden['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(biden_new[i])
        except TranscriptsDisabled:
            print("Transcripts disabled for video: %s" % biden_new[i])
        except NoTranscriptFound:
            print("No transcript found for video: %s" % biden_new[i])
        except VideoUnavailable:
            print("Video no longer available: %s" % biden_new[i])
    
    #add to json
    speeches.append(response_biden)

#HARRIS
if harris_new == [None]:
    pass
else: 
    #Get metadata       
    request_harris = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=harris_new
        )
    response_harris = request_harris.execute()
    print("Ran Harris request - 1 unit")
        
    #add candidate and captions
    for i in range(len(harris_new)):
        try:
            response_harris['items'][i]['candidate'] = 'harris'
            response_harris['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(harris_new[i])
        except TranscriptsDisabled:
            print("Transcripts disabled for video: %s" % harris_new[i])
        except NoTranscriptFound:
            print("No transcript found for video: %s" % harris_new[i])
        except VideoUnavailable:
            print("Video no longer available: %s" % harris_new[i])
    
    #add to json
    speeches.append(response_harris)
    
#PENCE
if pence_new == [None]:
    pass
else: 
    #Get metadata       
    request_pence = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=pence_new
        )
    response_pence = request_pence.execute()
    print("Ran Pence request - 1 unit")
        
    #add candidate and captions
    for i in range(len(pence_new)):
        try:
            response_pence['items'][i]['candidate'] = 'pence'
            response_pence['items'][i]['captions'] = YouTubeTranscriptApi.get_transcript(pence_new[i])
        except TranscriptsDisabled:
            print("Transcripts disabled for video: %s" % pence_new[i])
        except NoTranscriptFound:
            print("No transcript found for video: %s" % pence_new[i])
        except VideoUnavailable:
            print("Video no longer available: %s" % pence_new[i])
    
    #add to json
    speeches.append(response_pence)

#write JSON file
with open('speeches.json', 'w') as outfile:
     json.dump(speeches, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)