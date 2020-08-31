#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 23:25:54 2020

@author: maxwell
"""
import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
import datetime

#Get current dates to be used in search parameters (needs resolution)
today=datetime.date.today()
yesterday=today-datetime.timedelta(days=1)
daybefore=today-datetime.timedelta(days=2)
today_rfc3339=today.isoformat()+'T00:00:00+04:00' #+4:00 is needed to set to EST
yesterday_rfc3339=yesterday.isoformat()+'T00:00:00+04:00'
daybefore_rfc3339=daybefore.isoformat()+'T00:00:00+04:00'

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
service_account_file = "service_account.json"

    # Get credentials and create an API client
credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

#Biden Search
request = youtube.search().list(
        part="snippet",
        maxResults=1,
        publishedAfter=daybefore_rfc3339,
        publishedBefore=yesterday_rfc3339,
        q="biden full -trump",
        topicId="/m/05qt0",
        type="video",
        videoCaption="videoCaptionUnspecified",
        videoDuration="long"
    )
biden = request.execute()


#Trump Search
request = youtube.search().list(
        part="snippet",
        maxResults=1,
        publishedAfter=daybefore_rfc3339,
        publishedBefore=yesterday_rfc3339,
        q="trump full -biden",
        topicId="/m/05qt0",
        type="video",
        videoCaption="videoCaptionUnspecified",
        videoDuration="long"
    )
trump = request.execute()


#Extract video IDs to be pulled by create_records.py
biden_title = biden['items'][0]['snippet']['title'].lower()
trump_title = trump['items'][0]['snippet']['title'].lower()

#Do not add video if title seems to not be a speech
if 'biden' in biden_title and 'full' in biden_title:
    bidenID = biden['items'][0]['id']['videoId']
else:
    bidenID=None
if 'trump' in trump_title and 'full' in trump_title:
    trumpID = trump['items'][0]['id']['videoId']
else:
    trumpID=None