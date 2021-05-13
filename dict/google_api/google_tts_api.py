import os
from google.cloud import texttospeech as tts


def google_tts_api(word):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/maximmaximchuck/Downloads/quickstart-1554705327935-6b954f9a93e2.json"

    client = tts.TextToSpeechClient()

    synthesis_input = tts.SynthesisInput(text=word)

    voice = tts.VoiceSelectionParams(name='en-US-Wavenet-F', language_code="en-US")

    # Select the type of audio file you want returned
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    temp = "output_from_google_tts.mp3"
    print(f'*** [Save WordCard Method] Write Google TTS Object to file {temp}')
    with open(temp, "wb") as out:
        out.write(response.audio_content)
        full_path_temp = os.path.abspath(temp)
        print(f'*** [Save WordCard Method] Audio content written to file {full_path_temp}')

    return full_path_temp
