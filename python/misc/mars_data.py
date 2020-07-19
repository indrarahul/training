from random import randint

import requests

def fetch_pics(sol):
    api_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    params = {'sol':sol, 'api_key':'bCyTvplfgS7ArasuSNBATFYtmXEEENW1pb0yt8WV'}
    rsp = requests.get(api_url,params).json()
    pics = rsp['photos']

    img = pics[randint(0,len(pics)-1)]['img_src']
    print(img)