import os
from typing_extensions import Self
from aiohttp import request
import ffmpeg
import uuid
import sys
import random

from deepspeech import Model
from werkzeug.utils import secure_filename
import scipy.io.wavfile as wav

from typing import Optional
from fastapi import FastAPI, File, Request, Response

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
    
@app.post("/transcribe-encoding")
async def upload_file_encoding(data: bytes = File(...)):
    filename = secure_filename("test" + str(random.randrange(0,999)) + ".wav")
    fileLocation = os.path.join(os.path.dirname(__file__), filename)
    with open(fileLocation, "wb") as binary_file:
        binary_file.write(data)
        print(binary_file)
    convertedFile = normalize_file(fileLocation)
    os.remove(fileLocation)
    return {"result": await transcribe(convertedFile)}
    
@app.post("/transcribe")
async def upload_file(file: bytes = File(...)):
    filename = secure_filename("test" + str(random.randrange(0,999)) + ".wav")
    fileLocation = os.path.join(os.path.dirname(__file__), filename)
    with open(fileLocation, "wb") as binary_file:
        binary_file.write(file)
        print(binary_file)
    os.remove(fileLocation)
    return {"result": await transcribe(filename)}

@app.post("/transcribe-Unity")
async def upload_file_Unity(request: Request):
    form = await request.form()
    filename = secure_filename("test" + str(random.randrange(0,999)) + ".wav")
    fileLocation = os.path.join(os.path.dirname(__file__), filename)
    with open(fileLocation, "wb") as binary_file:
        binary_file.write(await form["file"].read())
        print(binary_file)
    os.remove(fileLocation)
    return {"result": await transcribe(filename)}
    
async def transcribe(filename):
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
