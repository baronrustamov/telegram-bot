'''
import os
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vidkey.json'


client = vision.ImageAnnotatorClient()
response = client.annotate_image({
  'image': {'source': {'image_uri': 'https://domashniirestoran.ru/wp-content/uploads/2017/10/lico-devushki.jpg'}},
  'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
})
print(response)
response = client.annotate_image({
  'image': {'source': {'image_uri': 'https://domashniirestoran.ru/wp-content/uploads/2017/10/lico-devushki.jpg'}},
  'features': [{'type_': vision.Feature.Type.IMAGE_PROPERTIES}]
})
print(response)
'''
'''
from prometheus_client import start_http_server, Summary
import random
import time

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
'''