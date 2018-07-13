#!usr/bin/python 3

## This module currently functions as a command line script.

import createAudio as ca 
import os
import speech_recognition as sr
import csv

print("""
#######################################################################
#   __                                             __                 #
#  /\ \  __          __                         __/\ \                #
#  \_\ \/\_\     __ /\_\    ____    ___   _ __ /\_\ \ \____     __    #
#  /'_` \/\ \  /'_ `\/\ \  /',__\  /'___\/\`'__\/\ \ \ '__`\  /'__`\  #
# /\ \L\ \ \ \/\ \L\ \ \ \/\__, `\/\ \__/\ \ \/ \ \ \ \ \L\ \/\  __/  #
# \ \___,_\ \_\ \____ \ \_\/\____/\ \____\\ \_\  \ \_\ \_,__/\ \____\ #
#  \/__,_ /\/_/\/___L\ \/_/\/___/  \/____/ \/_/   \/_/\/___/  \/____/ #
#                /\____/                                              #
#                \_/__/                                               #
#                                                                     #
#######################################################################

""")

filename = input("Which file would you like to process?  ")
print(" ")

try:
    ca.makeDirectory(filename)
    print("----  Directory Created!  Extracting Audio  ----")
except:
    print("---- Directory Already Exists! Extracting Audio  ----")
print(" ")

ca.createAudio(filename)

AUDIO_FILE = "audio/" + filename + "/audio.wav"


print("---- Contacting IBM Watson, please be patient ----")
print(" ")

## Leverage SpeechRecognition
r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

## ADD IBM USERNAME AND PASSWORD
username = IBM_USERNAME
password = IBM_PASSWORD

## Set Show_All to True in order to parse the JSON using the
## Timestampe parameter provided by Watson

try:
    results = r.recognize_ibm(audio, username=username, password=password, show_all=True)
except sr.UnknownValueError:
    print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from IBM Speech to Text service; {0}".format(e))

## create empty list for text processing
master_list = []

## process JSON, segmenting transcription by timestamp.
## For the purpose of closed captioning, this method
## currently segments words into three second chunks.

for i in range(len(results['results'])):
    section = results['results'][i]['alternatives'][0]['timestamps']
    
    start = section[0][1]
    end = section[-1][1]

    for mark in range(0, int((end-start)/3)+1):
            phrase = [(x[0],x[1]) for x in section if int((x[1]-start)/3)==mark]
            blurb = ' '.join((word for word, mark in phrase))
            stamp = phrase[0][1]

            grouped = [stamp, blurb]

            master_list.append(grouped)


## This formatting is specific to an enterprise-provided video repository.  For
## broader adoption, change to a SAMI file output.
with open("audio/" + filename + "/" + filename + ".csv", "w") as csvfile:
    filewriter = csv.writer(csvfile, delimiter = ",",
                            quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    filewriter.writerow(['Time', 'Type', 'Language', 'Title', 'Data'])
    
    for scripts in master_list:
        milliseconds = scripts[0] * 1000
        filewriter.writerow([milliseconds, 'caption', 'all', scripts[1], scripts[1]])
