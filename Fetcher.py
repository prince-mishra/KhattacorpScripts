from duplicity.globals import file_prefix

__author__ = 'prince'
import requests
import json
import sys
import os


def get_url_content(url):
    r = requests.get(url)
    text = r.text
    json_text = json.loads(text)
    return text, json_text


def create_and_write_to_file(folder, file_prefix, index, text):
    full_path = os.path.join(folder, file_prefix + '_' + str(index) + '.json')
    f = open(full_path, 'w+')
    f.write(text)
    f.close()


def construct_url(paging_url = '', page_id='', token=''):
    if paging_url:
        url = paging_url
    else:
        url = 'https://graph.facebook.com/' + page_id + '/posts/?access_token=' + token
    return url


def run(page_id, folder, file_prefix, token, max_pages=2000):
    #import rpdb2
    #rpdb2.start_embedded_debugger('p')
    dir_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    cur_page = 0
    url = construct_url(page_id=page_id, token=token)
    text, json_text = get_url_content(url)
    has_paging = json_text.get('paging')
    if has_paging:
        cur_page += 1
    while has_paging and cur_page < max_pages:
        print "Fetching page ", cur_page
        create_and_write_to_file(dir_path, file_prefix, cur_page, text)
        text, json_text = get_url_content(url)
        has_paging = json_text.get('paging')
        url = has_paging['next']
        cur_page += 1

if __name__ == "__main__":
    script, page_id, folder, file_prefix, token = sys.argv
    run(page_id, folder, file_prefix, token)