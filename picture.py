#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import base64
import httplib2
import subprocess
import urllib2, json, sys


from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


# 英単語を受け取って、日本語訳を並べた文字列を返す関数
def translate(phrase):
    # Glosbe API により、引数に与えられた単語の翻訳を取得
    # setURL
    from_lang = "en"# English
    dest_lang = "ja"# Japanese
    url = "https://glosbe.com/gapi/translate?from=" \
	+ from_lang + "&dest=" + dest_lang \
	+ "&format=json&phrase=" + phrase + "&pretty=true"
    response = urllib2.urlopen(url)
    json_data = response.read()
    json_dict = json.loads(json_data)

    return_txt = "" # これを返り値にする  
    tuc = json_dict["tuc"]# tuc: list
    return_txt = tuc[0]["phrase"]["text"]
    return return_txt

def main(photo_file):
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 5
                }]
            }]
        })
        response = service_request.execute()
        label = response['responses'][0]['labelAnnotations'][0]['description']
  	label_jp = translate(label)
	score = response['responses'][0]['labelAnnotations'][0]['score']
        print('Found label: %s(%s), score: %f for %s' % (label_jp, label, score, photo_file))
	
 	for label_num in range(1, 5): 
           label = response['responses'][0]['labelAnnotations'][label_num]['description']
  	   label_jp = translate(label)
	   score = response['responses'][0]['labelAnnotations'][label_num]['score']
           print('Found label: %s(%s), score: %f for %s' % (label_jp, label, score, photo_file))

        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
