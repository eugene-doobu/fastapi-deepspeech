import os
import ffmpeg
import uuid
import sys
import random

from deepspeech import Model
from werkzeug.utils import secure_filename
import scipy.io.wavfile as wav

from typing import Optional
from fastapi import FastAPI, File

app = FastAPI()

# model load
if os.path.isfile("models/deepspeech-0.9.3-models.pbmm"):
    print("Starting the DeepSpeech Frontend")
    ds = Model('models/deepspeech-0.9.3-models.pbmm')
    ds.enableExternalScorer('models/deepspeech-0.9.3-models.scorer')
elif os.path.isfile("/var/lib/deepspeech/models/deepspeech-0.9.3-models.pbmm"):
    ds = Model('/var/lib/deepspeech/models/deepspeech-0.9.3-models.pbmm')
    ds.enableExternalScorer('/var/lib/deepspeech/models/deepspeech-0.9.3-models.scorer')
else:
    sys.exit('No DeepSpeech Model found, please download one!')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/eugene")
async def upload_file_eugene(data: bytes = File(...)):
    filename = secure_filename("test" + str(random.randrange(0,999)) + ".wav")
    fileLocation = os.path.join(os.path.dirname(__file__), filename)
    with open(fileLocation, "wb") as binary_file:
        binary_file.write(data)
        print(binary_file)
    convertedFile = normalize_file(fileLocation)
    os.remove(fileLocation)
    return {"Hello": transcribe(convertedFile)}

def transcribe(filename):
    print("Starting transcription...")
    fs, audio = wav.read(os.path.join(os.path.dirname(__file__), filename))
    processed_data = ds.stt(audio)
    os.remove(os.path.join(os.path.dirname(__file__), filename))
    return processed_data

    # Use ffmpeg to convert our file to WAV @ 16k
def normalize_file(file: str):
    filename = str(uuid.uuid4()) + ".wav"
    fileLocation = os.path.join(os.path.dirname(__file__), filename)
    stream = ffmpeg.input(file)
    stream = ffmpeg.output(stream, fileLocation, acodec='pcm_s16le', ac=1, ar='16k')
    ffmpeg.run(stream)
    return filename
