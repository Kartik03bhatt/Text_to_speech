#Kartik Bhatt(RA2011028010162) GUI for Text to speech

import tkinter as tk
import boto3
import os
import sys
import PIL

from tempfile import gettempdir
from contextlib import closing
from tkinter import filedialog
from tkinter.filedialog import askopenfile

root = tk.Tk()  #create the window
root.geometry("400x240") #set dimension of window
root['background']='#2D383C'
root.title("Text to Speech using Amazon Polly")

textarea = tk.Text(root,height=10)  #create a text area handler in root window
textarea.pack() 

def convert():
    aws_console= boto3.session.Session(profile_name='awslab')  # programetically login aws IAM user
    client=aws_console.client(service_name='polly',region_name='ap-south-1')  #create a client that intract with aws service
    result=textarea.get("1.0","end")
    response=client.synthesize_speech(Engine='standard',OutputFormat='mp3',Text=result,VoiceId='Matthew')
    print(response)
    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output=os.path.join(gettempdir(),"speech.mp3")
            try:
                with open(output,"wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Could not find the stream")
        sys.exit(-1)
    if sys.platform=='win32':
        os.startfile(output)

button=tk.Button(root,height=1, width=10,text="Read",command=convert)
button.pack()

root.mainloop()