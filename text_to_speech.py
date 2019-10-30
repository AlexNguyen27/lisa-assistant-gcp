from pygame import time
import os

credential_path = 'apikey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# Audio for text+
def play_audio(file):
    from pygame import mixer
    mixer.init()

    mixer.music.load(file)
    mixer.music.play()

    while (mixer.music.get_busy()):
        continue

    mixer.music.load("holder.mp3")
    os.remove("output.mp3")


# for song
def play_song(file):
    from pygame import mixer
    mixer.init()

    while mixer.music.get_busy():
        time.Clock().tick(10)

    # mixer.init()
    mixer.music.load(file)
    mixer.music.play()


# play_song("./musics/Owl City - Fireflies-psuRGfAaju4.mp3")

def read_text(text):
    from google.cloud import texttospeech
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    # text = gTTS(text=x, lang='en')
    # with open(play_name, 'wb') as out:
    #     # Write the response to the output file.
    #     print('Reading Text')
    #     out.write(response.audio_content)
    #     print('Rewrite mp3 name...')
    #     os.rename(save_name, play_name)

    # out = gTTS(text=response.audio_content, lang='en')
    with open("output.mp3", 'wb') as out:
        # Write the response to the output file.
        print('Reading Text')
        out.write(response.audio_content)

    play_audio("output.mp3")
