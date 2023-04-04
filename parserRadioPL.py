from os import remove
import requests
from bs4 import BeautifulSoup
import re

sUrl = 'https://radiofm-online.com'
url = 'https://radiofm-online.com/radio-a-z'

with open(file = 'linkPlRadio.m3u', mode = 'w') as file:
    text_for_file = f"""#EXTM3U\n""" 
    file.write(text_for_file)

def add_links():
    """Start looking at the page with links to Internet radio pages."""
    soup = BeautifulSoup(requests.get(url).content, "html5lib")
    links_all = []
    for a_tag in soup.findAll("a"):
        a = str(a_tag.attrs.get("href"))
        if len(a) > 2 and a[0] == "/":
            link = f"{sUrl}{a}"
        else:
            continue
        links_all.append(link)
    return links_all

def gettingLinks():
    """Go through the internet radio pages and get the soup pages and wrinting in file *.json."""
    print("Recording is started!")
    for linkR in add_links():
        response = requests.get(linkR)
        for requestAllData in response:
            # print(response.content)
            with open(file = 'allData.json', mode = 'a') as file:
                text_for_file = f"""{str(requestAllData)}""" 
                file.write(text_for_file)
    print("Recording is complete!")

def washLink():
    """Selecting links and cleaning them up."""
    print("The laundry has begun!")
    comp = re.compile(r'stream={mp3:(\S*?)},')
    with open('allData.json', mode = 'r') as file:
        # for text in file.readlines():
        text = file.readlines()
    bad_link = comp.findall(str(text))
    for i in bad_link:
        i = i.replace("\\\'b\\\'", '')
        with open(file = 'linkPlRadio.m3u', mode = 'a') as file:
            text_for_file = f"""{i[1:-1]}\n"""
            file.write(text_for_file)
    remove('allData.json')

if __name__ == '__main__':
    try:
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            add_links()
            gettingLinks()
            washLink()
            print("Excellent! Job is done! Upload the file to the player. Enjoy listening to it!")
        else:
            print("Check settings!")
    except:
        exit()
