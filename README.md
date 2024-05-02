![logo-white](https://github.com/AkitaEllie/NusaStellar-TTSAI/assets/48817307/32be75f1-bfe7-47bf-8893-1b608964807c)


# NusaStellar TTS AI API Server

The repository for the backend server that powers the TTS engine of NusaStellar.


## Features

- Per-post and speaker audio retrieval and generation
- Multiple speakers


## API Reference

- #### Get list of speakers / AI voices

    ```http
    GET /speakers
    ```

- #### Generate Audio for Post.

    ```http
    POST /tts
    ```

    | Parameter | Type     | Description                       |
    | :-------- | :------- | :-------------------------------- |
    | `text`      | `string` | **Required**. The text to be spoken|
    | `speaker`      | `string` | **Required**. The ID of the speaker from /speakers |
    | `post`      | `string` | **Required**. The Post ID of the text |

- #### Generate Audio for Post.

    ```http
    GET /audio
    ```

    | Parameter | Type     | Description                       |
    | :-------- | :------- | :-------------------------------- |
    | `post`      | `string` | **Required**. The Post ID to get the audio of|
    | `speaker`      | `string` | **Required**. The ID of the speaker to request |
For more information and examples, please refer to the `/docs` endpoint on the server. 


## Run Locally
Please note that this project was made in Python 3.11.

Clone the project
```bash
  git clone https://github.com/AkitaEllie/NusaStellar-TTSAI
```
Go to the project directory

```bash
  cd NusaStellar-TTSAI
```
Install dependencies
```bash
  pip install -r requirements.txt
```
Find a TTS model externally, and name the main file `checkpoint.pth`, the speakers file `speakers.pth`, and the config `config.json` in the project root. We will not provide the models required.

If you are planning to run this with built-in models, then please replace line 14 of `main.py`. with
```py
ttsobj = TTS("tts_models/ind/fairseq/vits").to(device)
```

Start the server
```bash
  uvicorn main:app --reload
```


## Related

[NusaStellar Main Repository](https://github.com/oi-fen-link-sini)


## License

[MIT](https://choosealicense.com/licenses/mit/)

