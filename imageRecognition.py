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

def imageDetermin(photo_file, mode, compStr, rect):
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
                    'type': mode,
                    'maxResults': 5
                }]
            }]
        })
	response = service_request.execute()

	if mode == 'LOGO_DETECTION':
 		for label_num in range(0, 5): 
           		logo = response['responses'][0]['logoAnnotations'][label_num]['description']
			score = response['responses'][0]['logoAnnotations'][label_num]['score']
           		print('Found logo: %s, score: %f for %s' % (logo, score, photo_file))

	elif mode == 'LABEL_DETECTION':
		for label_num in range(0, 5): 
           		label = response['responses'][0]['labelAnnotations'][label_num]['description']
			score = response['responses'][0]['labelAnnotations'][label_num]['score']
           		print('Found label: %s, score: %f for %s' % (label, score, photo_file))
		
	elif mode == 'FACE_DETECTION':
           	joyVal = response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
		sorVal = response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
		angVal = response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
		sprVal = response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
		felList = [joyVal, sorVal, angVal, sprVal]
		if max(felList) == joyVal:
			str = 'JOY'
		elif max(felList) == sorVal:
			str = 'SORROW'
		elif max(felList) == angVal:
			str = 'ANGER'
		else:
			str = 'SURPRISE'

		print('face: %s' % str)
		if compStr == 'JOY':
			return str
		else:
           		return '-1'

	elif mode == 'TEXT_DETECTION':
		txt = response['responses'][0]['textAnnotations'][0]['description']
		print('txt: %s' % txt)

        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    imageDetermin(args.image_file, 'FACE_DETECTION', 'smile', rect)

