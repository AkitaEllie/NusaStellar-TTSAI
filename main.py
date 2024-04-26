from TTS.api import TTS
from g2p_id import G2P
from fastapi import HTTPException, FastAPI
from fastapi.responses import FileResponse
import torch
import os
from timeit import default_timer as timer
import json


g2p = G2P()

device = "cuda" if torch.cuda.is_available() else "cpu"
ttsobj = TTS(model_path='./checkpoint.pth', config_path='./config.json').to(device)


'''
good girl : 4190, 6207, 297, 264
boy 60, 3650, 1932, 
'''
description = """
NusaStellar TTS powers the AI voice of the NusaStellar website
"""
tags_metadata = [
    {
        "name": "Main",
        "description": "Everything the API has to offer.",
    }
]

app = FastAPI(   
    title="NusaStellar TTS API",
    description=description,
    summary="Make and Get spoken stories",
    version="0.9.0",
    openapi_tags=tags_metadata)


@app.get("/speakers", tags=["Main"],response_description="Array of Speakers as array in JSON",summary="Get speaker list")
def speakerlist():
    speakers = {"speakers":ttsobj.speakers}
    return json.dumps(speakers)


@app.post("/tts", tags=["Main"])
def tts(text:str, speaker:str, post:str):
    phoneme = g2p(text)
    if not os.path.exists(f"./{post}"):
        os.mkdir(f"./{post}")
    wav = ttsobj.tts_to_file(text=phoneme, speaker=speaker, file_path=f"./{post}/{speaker}.wav")
    return "issoke"

@app.get("/audio")
def audio(post:str, speaker:str):
    if not os.path.exists(f"./{post}"):
        raise HTTPException(status_code=404, detail="Unknown Post")
    if not os.path.exists(f"./{post}"):
        raise HTTPException(status_code=404, detail="Audio not generated yet!")
    audiofile = os.path.join("./",post,f"{speaker}.wav")
    print(audiofile)
    return FileResponse(audiofile)