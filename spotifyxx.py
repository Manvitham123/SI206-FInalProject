import os
import sys
import json
import webbrowser
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

#get the username from the terminal 
username = sys.argv[1]
scope="user-library-read user-read-recently-played"
client_id = '72fbe8b5ea87405286fbc89b66e33d7e'
client_secret = 'c021da7bc65a4d909e242dc52772637c'
redirect_uri = 'https://www.google.com/'
# manvitham

#erase cache and prompt for user permission 

try: 
    token = util.prompt_for_user_token(username, scope="user-library-read user-read-recently-played")
except:
    os.remove('.cache-{}'.format(username))
    token = util.prompt_for_user_token(username, scope, )

#create your object 


spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
followers = user['followers']['total']
playList = spotifyObject.current_user_playlists(limit=50, offset=0)

recently_played = spotifyObject.current_user_recently_played(limit=50, before=1689813253305)

def get_tracks_id(tracks):
  
  track_id = []
  
  for item in tracks:
    track_id.append(item['track']['id'])

  return track_id

#def get_tracks_audio_analysis(trackId):
   
  # trackAnalysis = []

   #for item in trackId:
   #   trackAnalysis.append(spotifyObject.audio_analysis(trackId))
  
   #return trackAnalysis
   

def get_tracks_artist(tracks):
  
  track_artist = []
  
  for item in tracks:
    track_artist.append(item['track']['album']['artists'][0]['name'])

  return track_artist

def get_tracks_name(tracks):
  
  track_names = []
  
  for item in tracks:
    
    track_names.append(item['track']['name'])

  return track_names

def get_date_played(tracks):
  
  dates_played = []
  
  for item in tracks:
    dates_played.append(item['played_at'])

  return dates_played

def mood_analysis(ids):
   tempo = []
   count = 0
   sum = 0
   for i in ids:
      analysis = spotifyObject.audio_features(i)
      tempo.append(analysis[0]["tempo"])
   for items in tempo:
      count = count + 1
      sum = items+sum
   mean = sum/count 

   if(180>mean>150):
      return 1
   elif(150>mean>120):
      return 2
   elif(120>mean>90):
      return 3
   elif((90>mean>40)):
      return 4

      
      

   
results = spotifyObject.current_user_recently_played()
with open('file.txt', 'w') as f:
    data = json.dumps(results, sort_keys=True, indent=4)
    f.write(data)
    
#tracks = get_tracks_name(results['items'])
#dates = get_date_played(results['items'])
#artist = get_tracks_artist(results['items'])
ids = get_tracks_id(results['items'])


#analysis = get_tracks_audio_analysis(id)
""""
while results['next'] and len(tracks) < 10:
    results = spotifyObject.next(results)
    tracks.extend(get_tracks_name(results['items']))
    dates.extend(get_date_played(results['items']))
    artist.extend(get_tracks_artist(results['items']))
    ids.extend(get_tracks_id(results['items']))
   """

    #analysis.extend(get_tracks_audio_analysis(id))
mood = mood_analysis(ids)
#print(tracks)
#print(artist)
#print(dates)
#print(id)

analysis1 = spotifyObject.audio_features(ids[0])
with open('file1.txt', 'w') as f:
    data = json.dumps(analysis1, sort_keys=True, indent=4)
    f.write(data)

if(mood == 1):
   print("you have been angry")
elif(mood==2):
    print("you have been excited")
elif(mood==3):
    print("you have been happy")
elif(mood==4):
    print("you have been sad")




#for i in data:
   # print(i)


#while True: 

   # print()
   # print(">>> Welcome to your spotify analytics")
   # print("you have"+ str(followers)+ " followers.")

#print(json.dumps(VARIABLE, sort_keys=True, indent=4))
#prints out json data in a fromat we can view 


