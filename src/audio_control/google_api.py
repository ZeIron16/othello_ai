
# Imports the Google Cloud client library

from google.cloud import speech
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import time

#global variables

fs = 16000  # Sample rate
seconds = 4  # Duration of recording
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] #alphabet
numbers = ['0','1','2','3','4','5','6','7','8','9'] #numbers
language = "en-US" #language code

#functions

def record() :
    """Record audio from the microphone and save it as a WAV file."""
    
    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    write("audio_file/output.wav", fs, myrecording)  # Save as WAV file
    print("end of recording")



def run_quickstart() -> speech.RecognizeResponse:
    """Read an audio file, send a request to the Google Speech-to-Text API, and print and return the transcribed text."""
    
    # Instantiates a client
    client = speech.SpeechClient()
    print("Authentication successful!")
    
    # The name of the audio file to transcribe
    with open("audio_file/output.wav", "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=fs,
        language_code=language,
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    if not response.results:
        #if no speech detected
        print("No speech detected or recognition failed.")
        return(None, None)
    else:
        #if speech detected return (transcript, confidence)
        for result in response.results:
            return (result.alternatives[0].transcript, result.alternatives[0].confidence)
           

def main():
    """While a valid answer is not given, record audio and run the quickstart function"""
    valid_answer = False
    while (not valid_answer):
        #record()
        transcript, confidence = run_quickstart()
        
        if confidence is not None and transcript is not None and confidence > 0.2 and len(transcript) == 2 : # 1st : quality check
            if transcript[0].lower() in alphabet and transcript[1] in numbers :
                print("Transcript:", transcript," Confidence:", confidence) # 2nd : user check
                print("Is the transcript correct?")
                satisfy = input("Enter Y or O : ")
                if satisfy == "Y" :
                    valid_answer = True
                    return(transcript)
            

for i in range(10) :
    time.sleep(5)
    main()
            
#main()