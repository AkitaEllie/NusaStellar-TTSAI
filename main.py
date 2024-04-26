from TTS.api import TTS
from g2p_id import G2P
from fastapi import HTTPException, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import torch
import os
import json


g2p = G2P()

device = "cuda" if torch.cuda.is_available() else "cpu"
ttsobj = TTS(model_path="./checkpoint.pth", config_path="./config.json").to(device)


"""
good girl : 4190, 6207, 297, 264
boy 60, 3650, 1932, 
"""
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
    openapi_tags=tags_metadata,
)


class Item(BaseModel):
    name: str
    price: float


@app.get(
    "/speakers",
    tags=["Main"],
    summary="Get speaker list",
    responses={
        200: {
            "description": "Array of Speakers as array in JSON",
            "content": {
                "application/json": {"example": {"speakers": ["speaker1", "speaker2"]}}
            },
        }
    },
)
def speakerlist():
    speaker = ttsobj.speakers
    speaker = [i.replace('"', "") for i in speaker]
    speakers = {"speakers": speaker}
    print(json.dumps(speakers))
    print(speakers)
    return json.dumps(speakers)


@app.post(
    "/tts",
    tags=["Main"],
    summary="Get Audio File for post",
    responses={
        200: {
            "description": "Status OK",
            "content": {"application/json": {"example": {"Detail": "All okay!"}}},
        },
        500: {
            "description": "Server Error",
            "content": {"application/json": {"example": {"Detail": "Exception Info"}}},
        },
    },
)
def tts(text: str, speaker: str, post: str):
    try:
        phoneme = g2p(text)
        if not os.path.exists(f"./{post}"):
            os.mkdir(f"./{post}")
        ttsobj.tts_to_file(
            text=phoneme, speaker=speaker, file_path=f"./{post}/{speaker}.wav"
        )
    except Exception as exp:
        raise HTTPException(status_code=500, detail=exp)
    return "issoke"


@app.get(
    "/audio",
    tags=["Main"],
    summary="Get Audio File for post",
    responses={
        200: {
            "description": "Status OK",
            "content": {"audio/wav": {"example": {"AudioFile"}}},
        },
        404: {
            "description": "Item not Found",
            "content": {"application/json": {"example": {"Detail": "Unknown Post / Audio Not Generated Yet"}}},
        },
    }
)
def audio(post: str, speaker: str):
    if not os.path.exists(f"./{post}"):
        raise HTTPException(status_code=404, detail="{\"Detail\": \"Unknown Post\"}")
    if not os.path.exists(f"./{post}/{speaker}.wav"):
        raise HTTPException(status_code=404, detail="{\"Detail\": \"Audio Not Generated Yet\"}")
    audiofile = os.path.join("./", post, f"{speaker}.wav")
    print(audiofile)
    return FileResponse(audiofile)
