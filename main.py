import pandas as pd
import os
import json
import requests
import pyttsx3


def TTS(inp):
    engine = pyttsx3.init()
    engine.setProperty('rate', engine.getProperty('rate') + 0)
    engine.save_to_file(inp, 'welcome.mp3')
    engine.runAndWait()
    os.system("start welcome.mp3")


def getInfo(rawFile):
    with open(rawFile) as f:
        data = f.read()

    js = json.loads(data)
    return js


def getHeaders():
    js = getInfo('mundane-addictionInfo.txt')
    auth = requests.auth.HTTPBasicAuth(js.get("ClientID"), js.get("SecretKey"))
    data = {
        'grant_type': 'password',
        'username': js.get('username'),
        'password': js.get('password')}
    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = res.json()['access_token']
    headers['Authorization'] = f'bearer {token}'

    return headers


def getUserComments(user):
    comments = ''
    res = requests.get(f'https://oauth.reddit.com/u/{user}/comments', headers=getHeaders())
    for comment in res.json()['data']['children']:
        comments += (comment['data']['body']) + "\n"

    return comments


def getPosts(subreddit, sort, numOfPosts, time):
    res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{sort}/',
                       headers=getHeaders(), params={'limit': f'{numOfPosts}', 't': f'{time}'})
    topPosts = pd.DataFrame()

    for post in res.json()['data']['children']:
        data = {
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'url': post['data']['url'],
            'postID': post['data']['id']
        }

        topPosts = pd.concat([topPosts, pd.Series(data)], axis=1, ignore_index=True)

    return topPosts


def getCommentsFromPost(posts, numOfComments, sortComments):
    df = pd.DataFrame()
    for i in range(len(posts.columns)):
        res = requests.get(f'https://oauth.reddit.com/r/{posts[i]["subreddit"]}/comments/{posts[i]["postID"]}',
                           headers=getHeaders(), params={f'depth': '1', 'sort': {sortComments}})


        data = []
        data.append(res.json()[0]['data']['children'][0]['data']['title'])

        for thread in res.json()[1]['data']['children'][0:numOfComments]:
            data.append(thread['data']['body'] + ". ")
        # print(pd.Series(data))

        df = pd.concat([df, pd.Series(data)], axis=1, ignore_index=True)

    return df


def getCommentsFromUrl(url, numOfComments, sortComments):
    url = url.split('/')

    df = pd.DataFrame()
    res = requests.get(f'https://oauth.reddit.com/r/{url[4]}/comments/{url[6]}',
                       headers=getHeaders(), params={f'depth': '1', 'sort': {sortComments}})

    data = []
    data.append(res.json()[0]['data']['children'][0]['data']['title'])

    for thread in res.json()[1]['data']['children'][0:numOfComments]:
        data.append(thread['data']['body'] + ". ")
        # print(pd.Series(data))

    df = pd.concat([df, pd.Series(data)], axis=1, ignore_index=True)

    return df


def createAudio(comments):
    redditVid = ""
    for c in range(len(comments.columns)):
        for r in range(len(comments)):
            redditVid += comments.iloc[r, c] + "\n"
        redditVid += "\n\n"

    print(redditVid)
    TTS(redditVid)

# TODO
# Video automation - create small clips then one vid
# try exception for app to make sure all fields are filled
# fix except in submit() and add url validator
# line 95
# add box for background music
# add selection box to crop video or not


# FORMATTING OPTIONS
formatting = False
if formatting:
    pd.set_option('display.max_columns', None)
    pd.set_option("max_colwidth", 999)


# posts = getPosts('askreddit', 'top', 2, 'today')
# comments = getCommentsFromUrl('https://www.reddit.com/r/college/comments/v9b8r5/whats_a_decent_backpack_i_can_get/?sort=top', 1, 'top')
# comments = getCommentsFromPost(posts, 2, 'top')
# print(posts)
# print(comments)
# createAudio(comments)

