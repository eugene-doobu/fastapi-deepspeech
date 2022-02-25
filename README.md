# fastapi-deepspeech
this repo is http-api to use deepspeech using fastapi

This project works on window and ubuntu

## Dependency

> pip install fastapi uvicorn ffmpeg ffmpeg-python deepspeech werkzeug scipy

## Installation

### Getting the pre-trained model
> wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
>
> wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

## use

> uvicorn main:app --reload --host=0.0.0.0 --port=8080

# Reference

[deepspeech_frontend](https://git.callpipe.com/fusionpbx/deepspeech_frontend)
