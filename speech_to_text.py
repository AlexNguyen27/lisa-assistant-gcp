from __future__ import division
import re
import sys
import os

credential_path = 'apikey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

from pygame import mixer

mixer.init()
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from threading import Thread
from six.moves import queue
from vision import detect_text
from text_to_speech import read_text
from text_to_speech import play_song
from web_parsing import web_parsing
from search_wikipedia import search_wikipedia
from weather import weather
import cv2

cap = cv2.VideoCapture(0)

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def camera():
    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        #cv2.imshow('Lisa View', frame)
        cv2.namedWindow('Lisa View', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Lisa View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Lisa View', frame)

        global stop_threads

        cv2.waitKey(1)
        if stop_threads:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# speech to text
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data)

# speech to text
def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            text = (transcript + overwrite_chars).lower().strip()
            global call_lisa
            if (text == 'hey lisa') or (text == 'hi lisa') or (text == 'lisa'):
                call_lisa = True
                read_text("Hi, how can I help you ?")
            elif call_lisa:
                lisa_command(text)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


# Check if Lía is called
call_lisa = False


# Lisa command
def lisa_command(text):
    global mixer
    if 'can you read this' in text:
        ret, frame = cap.read()
        cv2.imwrite("test1.jpg", frame)
        read_text(detect_text("test1.jpg"))
    elif 'what is in front of me' in text:
        ret, frame = cap.read()
        cv2.imwrite("test1.jpg", frame)
        localize_objects('test1.jpg')
    elif 'go to sleep' in text:
        if (mixer.music.get_busy):
            mixer.music.stop()
        # When everything done, release the capture
        global stop_threads
        global t1
        stop_threads = True
        t1.join()
        print('Lisa goes to sleep Zzz...')
        sys.exit(0)
    elif 'play the song' in text:
        if (mixer.music.get_busy):
            mixer.music.stop()
        # Thread to stop the web parsing when say "go to sleep"
        # Thread(target=web_parsing, args=[text.replace("play the song", "")]).start()
        Thread(target=web_parsing, args=[text.rpartition('play the song')[2]]).start()
    elif 'play again' in text:
        if (mixer.music.get_busy):
            mixer.music.stop()
        for topdir, dirs, files in os.walk("musics"):
            play_song('./musics/' + files[len(files) - 1])
    elif 'stop' in text:
        mixer.music.stop()
    elif 'search for' in text:
        if (mixer.music.get_busy):
            mixer.music.stop()
        Thread(target=search_wikipedia, args=[text.rpartition('search for')[2]]).start()
    elif 'what is the weather today' in text:
        if (mixer.music.get_busy):
            mixer.music.stop()
        Thread(target=weather).start()


# Object detection
def localize_objects(path):
    """Localize objects in the local image.
    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))

        if object_.score >= 0.7:
            read_text(object_.name)
            # print('Normalized bounding polygon vertices: ')
            # for vertex in object_.bounding_poly.normalized_vertices:
            #     print(' - ({}, {})'.format(vertex.x, vertex.y))


# Stream audio # speech to text
def stream_audio():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag #

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


# Main function
if __name__ == '__main__':
    stop_threads = False
    t1 = Thread(target=camera)
    t1.start()
    t2 = Thread(target=stream_audio)
    t2.start()