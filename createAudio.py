#!/usr/bin/python3

import os, sys
import subprocess

# Create Directory and pull audio from source video

def makeDirectory(filename):
    path = "audio/" + filename
    os.mkdir(path);
    
def createAudio(filename):
    command = "ffmpeg -i D:/SPROJ/Transcriber/vids/" + filename + ".mp4 -ab 160k -ac 2 -ar 44100 -vn D:/SPROJ/Transcriber/audio/" + filename + "/audio.wav"
    subprocess.run(command, shell=True, check=True)





