#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from connect_dynamo import *
import os
import json
#basepath = '.media/'
basepath = '/tmp'
client=boto3.client('rekognition')

def detect_labels_local_file(photo):

    fullreturnarray = []
    keyreturnarray = []
    tsaimage = []
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        
    print('Detected labels in ' + photo)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
        tsaimage =  get_tsaimage(label['Name'])
        if label['Confidence'] < 40:
            print('recognition confidence below 40')
            break

        if tsaimage:
         print("Get tsa image succeeded for " + label['Name'])
         partialCat = tsaimage[0]["id"]["S"]
         print(partialCat)
         
         exists = partialCat in keyreturnarray
         
         if exists == False :
          fullreturnarray.append(tsaimage[0])
          keyreturnarray.append(partialCat)
         

    return fullreturnarray

def detect_ppe_local_file(photo):
    ppeReturnArray = []
    with open(photo, 'rb') as image:
        imageBytes = bytearray(image.read())
        response = client.detect_protective_equipment(Image={'Bytes': imageBytes},
            SummarizationAttributes={
            'MinConfidence': 90,
            'RequiredEquipmentTypes': [
                'FACE_COVER',
                'HEAD_COVER',
                'HAND_COVER',
            ]
        }
    )
    print(response)
    ppeReturnArray.append(response)
    return ppeReturnArray
    

def main():
    photo='.media/Coat.jpg'

    for entry in os.listdir(basepath):
     if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)
        label_count=detect_labels_local_file(basepath + entry)
        print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()



