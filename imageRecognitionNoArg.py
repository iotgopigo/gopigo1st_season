#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import base64
import httplib2
import subprocess
import urllib2, json
import numpy as np
import cv2
import codecs
import sys
sys.stdin = codecs.getreader("utf-8")(sys.stdin)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

def imageDetermin(mode, compStr, rect):
    """Run a label request on a single image"""
    img = cv2.imread('nametag1.jpg', 0)
    cv2.imshow('nametag1.jpg', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)

    with  open(img, 'rt').read() as image:
        image_content = base64.b64encode(image)
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
	size = len(response['responses'][0])
        
        print "size:" + str(size)
        if size >= 1:

	  if mode == 'LOGO_DETECTION':
	    for label_num in range(0, 5): 
	      logo = response['responses'][0]['logoAnnotations'][label_num]['description']
	      score = response['responses'][0]['logoAnnotations'][label_num]['score']
	      print('Found logo: %s, score: %f for %s' % (logo, score, photo_file))
	    if  logo == compStr:
	      print('logo-success')

	  elif mode == 'LABEL_DETECTION':
	    for label_num in range(0, 5): 
	      label = response['responses'][0]['labelAnnotations'][label_num]['description']
	      score = response['responses'][0]['labelAnnotations'][label_num]['score']
	      print('Found label: %s, score: %f for %s' % (label, score, photo_file))
            if  label == compStr:
	      print('label-success')

		
	  elif mode == 'FACE_DETECTION':
	    joyVal = response['responses'][0]['faceAnnotations'][0]['joyLikelihood']
	    sorVal = response['responses'][0]['faceAnnotations'][0]['sorrowLikelihood']
	    angVal = response['responses'][0]['faceAnnotations'][0]['angerLikelihood']
	    sprVal = response['responses'][0]['faceAnnotations'][0]['surpriseLikelihood']
	    felList = [joyVal, sorVal, angVal, sprVal]
	    if max(felList) == joyVal:
	      reStr = 'JOY'
	    elif max(felList) == sorVal:
	      reStr = 'SORROW'
	    elif max(felList) == angVal:
	      reStr = 'ANGER'
	    else:
	      reStr = 'SURPRISE'

	    print('face: %s' % reStr)
	    if compStr == 'JOY':
	      return reStr
	    else:
	      return '-1'

	  elif mode == 'TEXT_DETECTION':
	    txt = response['responses'][0]['textAnnotations'][0]['description']
	    print('txt: %s' % txt)
	
	  return 0
	
	else:
	  return -1

        

if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument('image_file', help='The image you\'d like to label.')
    #args = parser.parse_args()
    rect = [1, 2, 3]
    imageDetermin('FACE_DETECTION', 'JOY', rect)
    imageDetermin('LABEL_DETECTION', 'dog', rect)
    imageDetermin('TEXT_DETECTION', 'group', rect)
