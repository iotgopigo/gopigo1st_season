#! /usr/bin/python
# -*- coding: utf-8 -*-

#
import base64
import httplib2
import urllib2, json
import numpy as np
import cv2
import sys

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

#
# The url template to retrieve the discovery document for trusted testers.
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
MAX_NUM_IMAGE_DETECTION = 5

inputFlag = False
filename = 'panasonic2.jpg'

def getImage():
    print 'test'
    return cv2.imread('panasonic2.jpg', 0)
#
def imgeDeterminParamCheck(mode):
    if mode == 'LOGO_DETECTION':
        return True
    elif mode == 'LABEL_DETECTION':
        return True
    elif mode == 'FACE_DETECTION':
        return True
    elif mode == 'TEXT_DETECTION':
        return True
    else: 
        return False

#
def imageDetermin(mode, compStr, rect):
    del rect[:]
    rect.append(-1)
    rect.append(-1)
    rect.append(-1)
    rect.append(-1)
    
    if imgeDeterminParamCheck(mode) == False:
        return '-1'

    #
    """Run a label request on a single image"""
    if inputFlag == True:
        img = cv2.imread(filename, 0)
    else:
        img = getImage()
    if img is None:
        return '-1'

    #
    credentials         = GoogleCredentials.get_application_default()
    service             = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)
    result, imgencode   = cv2.imencode('.jpg', img)
    data                = np.array(imgencode)
    image_content       = base64.b64encode(data.tostring())
    service_request     = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': mode,
                'maxResults': MAX_NUM_IMAGE_DETECTION
            }]
        }]
    })
    response = service_request.execute()
    
    detectFlag = False
    detectList = []
    annotations = None

    #
    size = len(response['responses'][0])
    print "size:" + str(size)
    if size >= 1:
        #        
        if mode == 'LABEL_DETECTION':
            annotations = response['responses'][0]['labelAnnotations']
            for label_num in range(0, len(annotations)):
                label = annotations[label_num]['description']
                score = annotations[label_num]['score']
                print('Found label: %s, score: %f' % (label, score))
                detectList.append(label)
                if  label == compStr:
                    detectFlag = True
                    reStr = label
                    break
            if detectFlag == False:
                reStr = detectList[0]
                
            return reStr
        #
        elif mode == 'LOGO_DETECTION':
            annotations = response['responses'][0]['logoAnnotations']
            for label_num in range(0, len(annotations)):
                logo = annotations[label_num]['description']
                score = annotations[label_num]['score']
                print('Found logo: %s, score: %f' % (logo, score))
                detectList.append(logo)
                if  logo == compStr:
                    detectFlag = True
                    reStr = logo
                    break
            if detectFlag == False:
                reStr = detectList[0]
        #
        elif mode == 'FACE_DETECTION':
            annotations = response['responses'][0]['faceAnnotations']
            joyVal = annotations[0]['joyLikelihood']
            angVal = annotations[0]['angerLikelihood']
            sorVal = annotations[0]['sorrowLikelihood']
            sprVal = annotations[0]['surpriseLikelihood']
            print ('joyVal %s' % joyVal)
            print ('angVal %s' % angVal)
            print ('sorVal %s' % sorVal)
            print ('sprVal %s' % sprVal)
            if joyVal == 'VERY_LIKELY' or joyVal == 'LIKELY' or joyVal == 'POSSIBLE':
                reStr = 'JOY'
            elif angVal == 'VERY_LIKELY' or angVal == 'LIKELY' or joyVal == 'POSSIBLE':
                reStr = 'ANGER'
            elif sorVal == 'VERY_LIKELY' or sorVal == 'LIKELY' or joyVal == 'POSSIBLE':
                reStr = 'SORROW'
            elif sprVal == 'VERY_LIKELY' or sprVal == 'LIKELY' or joyVal == 'POSSIBLE':
                reStr = 'SURPRISE'
            else :
                reStr = 'NORMAL'
        #
        elif mode == 'TEXT_DETECTION':
            annotations = response['responses'][0]['textAnnotations']
            txt = annotations[0]['description']
            print ('txt:%s' % txt )
            if compStr in txt:
                reStr = compStr
            else: 
                reStr = '-1'
       
        #
        print annotations[0]['boundingPoly']['vertices']
        if annotations[0]['boundingPoly']['vertices'][0].has_key('x'):
            rect[0] = annotations[0]['boundingPoly']['vertices'][0]['x']
        else :
            rect[0] = 0
        if annotations[0]['boundingPoly']['vertices'][0].has_key('y'):
            rect[1] = annotations[0]['boundingPoly']['vertices'][0]['y']
        else :
            rect[1] = 0
        rect[2] = annotations[0]['boundingPoly']['vertices'][2]['x']
        rect[3] = annotations[0]['boundingPoly']['vertices'][2]['y']

        #
        cv2.rectangle(img, (rect[0],rect[1]), (rect[2],rect[3]), (255,255,255), 5)
        cv2.imshow('nametag1.jpg', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return reStr
    #
    else :
        return '-1'

        
if __name__ == '__main__':

    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    if argc == 2:
        inputFlag = True
        filename = argvs[1]
        
    rect = []

    print 'FACE_DETECTION'
    text = imageDetermin('FACE_DETECTION', 'JOY', rect)
    print text
    print rect
    print ''

    print 'LABEL_DETECTION'
    text = imageDetermin('LABEL_DETECTION', 'dog', rect)
    print text
    print rect
    print ''

    print 'TEXT_DETECTION'
    text = imageDetermin('TEXT_DETECTION', 'Staff', rect)
    print text
    print rect
    print ''
 
    print 'LOGO_DETECTION'
    text = imageDetermin('LOGO_DETECTION', 'panasonic', rect)
    print text
    print rect

