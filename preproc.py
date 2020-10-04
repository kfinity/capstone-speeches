#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 20:16:54 2020

Various preprocessing functions

@author: kfinity
"""

import pandas as pd
import numpy as np
import json
import nltk

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import os
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account

# Given the full JSON contents of our "speeches.json" file, return a dataframe
def create_bow(json):
    json=tag_interviews(json)
    df=pd.DataFrame(columns=['id','speaker','date','speech','title','transcript_type'])
    for i in range(len(json)): # for each entry...
        for k in range(len(json[i]['items'])): #for each speech...
            id = json[i]['items'][k]['id']
            speaker = json[i]['items'][k]['candidate']
            date = json[i]['items'][k]['snippet']['publishedAt']
            title = json[i]['items'][k]['snippet']['title']
            transcript_type = json[i]['items'][k]['type']
            try:
                captions = json[i]['items'][k]['captions']
            except KeyError:
                captions = None
            if captions != None:
                just_text = [j['text'] for j in captions]
                speech = ' '.join(just_text)
            row = {"id": id, "speaker": speaker, "date": date, "speech":speech, "title":title,"transcript_type": transcript_type}
            df = df.append(row,ignore_index=True)
    
    # drop speeches with no transcript
    df = df.dropna()
    # drop any duplicate videoIds
    df = df.reset_index().drop_duplicates(subset=['id'])\
      .sort_values('date').set_index('id')
    return df

# Given a dataframe, break up the speech into tokens
def tokenize(df, remove_pos_tuple=False):
    
    df = df.reset_index().set_index(['id','speaker'])

    df = df.speech\
        .apply(lambda x: pd.Series(nltk.pos_tag(nltk.WhitespaceTokenizer().tokenize(x))))\
        .stack()\
        .to_frame()\
        .rename(columns={0:'pos_tuple'})
    
    # Grab info from tuple
    df['pos'] = df.pos_tuple.apply(lambda x: x[1])
    df['token_str'] = df.pos_tuple.apply(lambda x: x[0])
    if remove_pos_tuple:
        df = df.drop('pos_tuple', 1)
        
    df['term_str'] = df['token_str'].str.lower().str.replace('[\W_]', '')
    
    df.index.names = ['id','speaker','token_id']
        
    return df


# Create a TFIDF table
def create_tfidf(token,bag,count_method='n',tf_method='sum',idf_method='standard'):
    BOW = token.groupby(bag+['term_id']).term_id.count().to_frame().rename(columns={'term_id':'n'})
    BOW['c'] = BOW.n.astype('bool').astype('int')
    DTCM = BOW[count_method].unstack().fillna(0).astype('int')
    if tf_method == 'sum':
        TF = DTCM.T / DTCM.T.sum()
    elif tf_method == 'max':
        TF = DTCM.T / DTCM.T.max()
    elif tf_method == 'log':
        TF = np.log10(1 + DTCM.T)
    elif tf_method == 'raw':
        TF = DTCM.T
    elif tf_method == 'double_norm':
        TF = DTCM.T / DTCM.T.max()
        TF = tf_norm_k + (1 - tf_norm_k) * TF[TF > 0] # EXPLAIN; may defeat purpose of norming
    elif tf_method == 'binary':
        TF = DTCM.T.astype('bool').astype('int')
    TF = TF.T
    DF = DTCM[DTCM > 0].count()
    N = DTCM.shape[0]
    if idf_method == 'standard':
        IDF = np.log10(N / DF)
    elif idf == 'max':
        IDF = np.log10(DF.max() / DF) 
    elif idf_method == 'smooth':
        IDF = np.log10((1 + N) / (1 + DF)) + 1 # Correct?
    TFIDF = TF * IDF
    return TFIDF

#Identify which speeches are interviews
def find_interviews(json):
    videoIDs = []
    for i in range(len(json)): # for each entry...
        for k in range(len(json[i]['items'])): #for each speech...
            if 'interview' in json[i]['items'][k]['snippet']['title'].lower():
                videoIDs.append(json[i]['items'][k]['id'])
            else:
                pass
    return videoIDs

def tag_interviews(json):
    interviews = find_interviews(json)
    for i in range(len(json)): # for each entry...
        for k in range(len(json[i]['items'])): #for each speech...
            if json[i]['items'][k]['id'] in interviews:
                json[i]['items'][k]['type'] = 'interview'
            else:
                json[i]['items'][k]['type'] = 'speech'
    return json

def remove_speech(videoID, json):
    for i in range(len(json)): # for each entry...
        for k in range(len(json[i]['items'])): #for each speech...
            if json[i]['items'][k]['id'] == videoID:
                del json[i]['items'][k]
                break
        else:
            continue
        break
    print("Don't forget to save your new json!")
    
# download captions and youtube details for a single videoId
# match the json structure from "create_records.py"
def build_video_details(videoId, candidate):
    captions = None
    
    if 'youtube' not in locals():
        SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        service_account_file = "service_account.json"
        
        # Get credentials and create an API client
        credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=SCOPES)
        youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)
    
    request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=videoId
        )
    response = request.execute()
    
    try:
        captions = YouTubeTranscriptApi.get_transcript(videoId)
    except TranscriptsDisabled:
        print("Transcripts disabled for video: %s" % videoId)
    except NoTranscriptFound:
        print("No transcript found for video: %s" % videoId)
    except VideoUnavailable:
        print("Video no longer available: %s" % videoId)
    
    response['items'][0]['candidate'] = candidate
    response['items'][0]['captions'] = captions
    
    return response
    
# add a single speech to the json
def add_speech(videoId, candidate, json):
    
    for i in range(len(json)): # for each entry...
        for k in range(len(json[i]['items'])): #for each speech...
            if json[i]['items'][k]['id'] == videoId:
                print("videoID {} already exists in speeches json")
                exit
    # is a new speech, can add it...
    resp = build_video_details(videoId, candidate)
    if resp['items'][0]['captions'] != None:
        json.append(resp)
