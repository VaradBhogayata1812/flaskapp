import os
import json
import requests
from flask import Flask, request, render_template

app = Flask(__name__)
app.debug = True

api_key = os.getenv('API_KEY')

def fetch_movies_from_api():
    api_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        print("Failed to fetch movies")
        return []

@app.route('/')
def home_page():
    movies = fetch_movies_from_api()
    return render_template('movies_list.html', movies=movies)

@app.route('/Video/<video>')
def video_page(video):
    print (video)
    url = 'http://34.88.51.222/myflix/videos?filter={"video.uuid":"'+video+'"}'
    headers = {}
    payload = json.dumps({ })
    print (request.endpoint)
    response = requests.get(url)
    print (url)
    if response.status_code != 200:
      print("Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message']))
      return "Unexpected response: {0}. Status: {1}. Message: {2}".format(response.reason, response.status, jResp['Exception']['Message'])
    jResp = response.json()
    print (type(jResp))
    print (jResp)
    for index in jResp:
        for key in index:
           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      video=index[key][key2]
                  if (key2=="file"):
                      videofile=index[key][key2]
                  if (key2=="pic"):
                      pic=index[key][key2]
    return render_template('video.html', name=video,file=videofile,pic=pic)

@app.route('/videos')
def videos_page():
    url = "http://34.88.51.222/myflix/videos"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Unexpected response: {response.reason}. Status: {response.status}")
        return f"Unexpected response: {response.reason}. Status: {response.status}"
    jResp = response.json()
    html = "<h2>Your Videos</h2>"
    for index in jResp:
       #print (json.dumps(index))
       print ("----------------")
       for key in index:

           if (key !="_id"):
              print (index[key])
              for key2 in index[key]:
                  print (key2,index[key][key2])
                  if (key2=="Name"):
                      name=index[key][key2]
                  if (key2=="thumb"):
                      thumb=index[key][key2]
                  if (key2=="uuid"):
                      uuid=index[key][key2]  
              html=html+'<h3>'+name+'</h3>'
              ServerIP=request.host.split(':')[0]
              html=html+'<a href="http://'+ServerIP+'/Video/'+uuid+'">'
            #   html=html+'<img src="http://34.88.51.222/pics/'+thumb+'">'
              html=html+"</a>"        
              print("=======================")

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
