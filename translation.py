import os

credential_path = 'apikey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
import six

def translate_language(text):
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language='vi')

    # print(u'Text: {}'.format(result['input']))
    # print(u'Translation: {}'.format(result['translatedText']))
    # print(u'Detected source language: {}'.format(
    #     result['detectedSourceLanguage']))
    return result['translatedText'];


