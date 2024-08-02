# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "ef03ba80a5a245db95a22aef86f8476b"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("./test.m4a")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)
