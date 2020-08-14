import os

credential_path = 'apikey.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Detected Texts:')
    # print(texts[0].description.replace("\n", " "))

    if (len(texts)):
        return texts[0].description.replace("\n", " ")
    return ""