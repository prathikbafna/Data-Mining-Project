from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import sys
import pymongo
from pymongo import MongoClient
import dns
import datetime
from dateutil.parser import parse
from youtube_comments import *

client = pymongo.MongoClient("mongodb+srv://prathikbafna0:gafA4AoTOraqh5RK@cluster0.t3qhk6n.mongodb.net/Social_media_data?retryWrites=true&w=majority")
db = client.Social_media_data
YouTube = db.youTube


def Category(Id):
    switcher = {
        1  : "Film & Animation",
        2  : "Autos & Vehicles",
        10 : "Music",
        15 : "Pets & Animals",
        17 : "Sports",
        19 : "Travel & Events",
        20 : "Gaming",
        22 : "People & Blogs",
        23 : "Comedy",
        24 : "Entertainment",
        25 : "News & Politics",
        26 : "Howto & Style",
        27 : "Education",
        28 : "Science & Technology",
        29 : "Nonprofits & Activism"
    }
    return switcher.get(Id, "None")

def youtube_search(q, max_results,order="date", token=None, location=None, location_radius=None):
    DEVELOPER_KEY = "AIzaSyCLa0LoJiVAWWEX-BH4prLyldw13r0AbUI"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    #Returns a list of channel activity events that match the request criteria.
    #For example, you can retrieve events associated with a particular channel or with the user's own channel.

    #https://developers.google.com/youtube/v3/docs/activities/list

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    '''{
          "kind": "youtube#activityListResponse",
          "etag": etag,
          "nextPageToken": string,
          "prevPageToken": string,
          "pageInfo": {
            "totalResults": integer,
            "resultsPerPage": integer
          },
          "items": [
            activity Resource
          ]
        }'''


    for search_result in search_response.get("items", []):

        if search_result["id"]["kind"] == "youtube#video":
            response = youtube.videos().list(
            part="statistics,snippet", # Part signifies the different types of data you want
            id = search_result['id']['videoId']).execute()


            #todo sentiment analysis
            Sentiment = "todo"
            if 'likeCount' in response['items'][0]['statistics'].keys():
                LikeCount = response["items"][0]["statistics"]["likeCount"]
            else:
                LikeCount = -1
            if 'dislikeCount' in response['items'][0]['statistics'].keys():
                DislikeCount = response["items"][0]["statistics"]["dislikeCount"]
            else:
                DislikeCount = -1
            if 'commentCount' in response['items'][0]["statistics"].keys():
                CommentCount = response["items"][0]["statistics"]["commentCount"]
            else:
                CommentCount = 0
            print(search_result['id']['videoId'])

            COMMENTS = comments_(search_result['id']['videoId'])
            if len(COMMENTS) == 0:
                COMMENTS = {}

        if 'tags' in response['items'][0]['snippet'].keys():
            Tags = response['items'][0]['snippet']['tags']
        else:
            Tags = []
        youtube_data = {
        'source':'youtube',
        'id':str(search_result['id']['videoId']),
        'text':search_result['snippet']['title'],
        'tag' : q,
        "sentiment":Sentiment,
        'created_time': parse(datetime.datetime.strptime(response['items'][0]['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')),
        'url': "http://www.youtube.com/watch?v="+str(search_result['id']['videoId']),
        "spam":False,
        'misc':{
        'tags': Tags,
        'channelId': str(response['items'][0]['snippet']['channelId']),
        'channelTitle': response['items'][0]['snippet']['channelTitle'],
        'categoryId':int(response['items'][0]['snippet']['categoryId']),
        'category':Category(int(response['items'][0]['snippet']['categoryId'])),
        'viewCount':int(response['items'][0]['statistics']['viewCount']),
        'likeCount':int(LikeCount),
        'dislikeCount':int(DislikeCount),
        'commentCount':int(CommentCount),
        'favoriteCount':int(response['items'][0]['statistics']['favoriteCount']),
        'comments': COMMENTS},
        "createdAt": datetime.datetime.now(), "updatedAt": datetime.datetime.now()
        }


    return youtube_data

def Video_Search(Search,max_results=50):
    return youtube_search(Search,max_results)
