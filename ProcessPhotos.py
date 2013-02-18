__author__ = 'prince'
import requests
import json
import os
import sys

from PIL import Image
from StringIO import StringIO


def get_picture_from_url(url):
    r = requests.get(url)
    i = Image.open(StringIO(r.content))
    filename = os.path.basename(url)
    print "Now saving ", filename
    i.save(filename)


def run(path):
    for item in os.listdir(path):
        full_name = os.path.join(path, item)
        try:
            file_handle = open(full_name, 'r')
            data = file_handle.read()
            file_handle.close()
            json_data = json.loads(data)
        except Exception, fault:
            print "cannot open file. ", file_handle, "\n", str(fault)
            continue
        #print j['data'][0]['message']
        for entry in json_data['data']:
            try:
                if entry['type'] == 'photo':
                    url = entry['picture']
                    s = os.path.splitext(url)
                    base = s[0][:-1] + 'n'
                    new_url = base + s[1]
                    print new_url
            except Exception, fault:
                print "Error in data.\n", entry, "\n", str(fault)
                continue

def create_pictures_from_links(path):
    path = os.path.join(os.getcwd(), path)
    os.chdir(path)
    link = raw_input()
    while (link):
        get_picture_from_url(link)
        link = raw_input()

if __name__=="__main__":
    path = sys.argv[1]
    #run(path)
    create_pictures_from_links(path)