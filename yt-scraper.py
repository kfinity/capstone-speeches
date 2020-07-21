
import pandas as pd
import requests
import json
import pymongo
from youtube_transcript_api import YouTubeTranscriptApi

# Part 1 - Setup

# connect to mongodb
myclient = pymongo.MongoClient("mongodb://localhost/")
db = myclient["speeches"]

# Part 2 - Build library of videos

# TODO - replace this section with a search to pull speeches
# define youtube playlists to pull video transcripts from
# playlist_id, candidate, source_description
sources = [['PLB92o2PvjqnfXeskcxX3GR6alCzdVFHjQ','Biden','Joe Biden Official YouTube Channel. Playlist: Livestreams, Speeches, and Debates'],
           ['PLKOAoICmbyV2XOjXa9u00njJ6fTLpOK5x','Trump','Donald J Trump Official YouTube Channel. Playlist: Trump Rallies']]

# pull the video IDs, titles, etc from the playlist
def playlist_index(source):
    # api key AIzaSyC7mEGnVGAFmoy23HdHJo877vZQ7DsYLeg
    pl_df = pd.DataFrame()
    next_page_str = ""
    while True: # loop through pages of 25 results
        r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?" + 
                         "part=id%2CcontentDetails%2Csnippet&" +
                         "maxResults=25&" + # default of 5
                         "playlistId=" + source[0] + "&" + next_page_str +
                         "key=AIzaSyC7mEGnVGAFmoy23HdHJo877vZQ7DsYLeg", 
                         headers = {'Accept': 'application/json'})
        if r.status_code != 200:
            print("Error for playlist " + source[0])
            print(r.text)
            break
        pl_json = json.loads(r.text)
        df = pd.DataFrame(
            [i['snippet']['resourceId']['videoId'],
             i['snippet']['publishedAt'],
             i['snippet']['title']] for i in pl_json['items']
        )
        df.columns = ['videoId','publishedAt','title']
        df['source'] = "youtube"
        df['candidate'] = source[1]
        df['source_desc'] = source[2]
        pl_df = pl_df.append(df)
        if "nextPageToken" not in pl_json:
            break
        next_page_str = "pageToken="+ pl_json['nextPageToken'] + "&" 
    # clean up playlist
    pl_df = pl_df
    return pl_df
    
# set up a library of documents

try:
    cursor = db["library"].find()
    library = pd.DataFrame(list(cursor)).drop(columns="_id")
except: # can't load from mongodb, create new collection
    print("Couldn't load library, creating new one")
    library = pd.DataFrame()
    db.create_collection('library')
for s in sources:
    library = library.append(playlist_index(s))
    
# remove all the duplicates added
library = library.sort_values(["publishedAt"], ascending=False)\
        .drop_duplicates(["videoId"],keep="first")


# write new entries to mongodb

cursor = db["library"].find()
curlist = list(cursor)
if len(curlist) == 0:
    old_lib = pd.DataFrame(columns=library.columns)
else:
    old_lib = pd.DataFrame(curlist).drop(columns="_id") # existing library entries

library=library.set_index(['videoId']) 
new_lib = library[~library.index.isin(old_lib.videoId)].reset_index() # new entries only; might be none

print("Writing {} new records to collection".format(new_lib.shape[0]))
records = json.loads(new_lib.to_json(orient="records")) # convert new entries to JSON
if len(records) > 0:
    db["library"].insert_many(records) # write to db

library = library.reset_index()

# Part 3 - Build df of raw transcripts

# load existing doc from a file if it exists
    
try:
    cursor = db["transcripts"].find()
    curlist = list(cursor)
    if len(curlist) == 0:
        transcripts = pd.DataFrame(columns=["text","start","duration","videoId"])
    else:
        transcripts = pd.DataFrame(curlist).drop(columns="_id") # existing raw entries
    
except: # can't load from mongodb, create new collection
    print("Couldn't load library, creating new one")
    transcripts = pd.DataFrame()
    db.create_collection('transcripts')

from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

n = 0
for v in library['videoId']:
    if 'videoId' in transcripts.columns and transcripts[transcripts['videoId'] == v]['videoId'].count() > 0:
        n = n + 1
        continue # already exists, don't overwrite it. skip to next loop
    try:
        t = YouTubeTranscriptApi.get_transcript(v)
        rec = {"videoId": v, "transcript": t}
        db["transcripts"].insert_one(rec)
    except TranscriptsDisabled:
        print("Transcripts disabled for video: %s" % v)
    except NoTranscriptFound:
        print("No transcript found for video: %s" % v)
    n = n + 1
    if n % 10 == 0:
        print(n) # print progress numbers
        
print("Done")
