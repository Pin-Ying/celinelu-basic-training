from bs4 import BeautifulSoup
import requests
from datetime import datetime

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

# 目標看版
# Stock
# Baseball
# NBA
# HatePolitics
# Lifeismoney

all_boards = ['Stock','Baseball','NBA','HatePolitics','Lifeismoney']

# 某 <board> url(最新) https://www.ptt.cc/bbs/<board>/index.html

