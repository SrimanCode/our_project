import os
import requests
import urllib.parse


from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

from google.cloud import storage
from datetime import datetime, timedelta

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(link):
    """Look up quote for symbol."""

    # Contact API
    try:
        #api_key = os.environ.get("API_KEY")
        url = []
        client = HumeBatchClient("ZdiSGcM78YnnyJH0PX2Pm6Ovwov1zpWPFaJfSztrmpGbqrvZ")
        configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
        url.append(link)
        job = client.submit_job(url, configs)
        job.await_complete()
        emoList = job.get_predictions()

        anxiety_score = None
        guilt_score = None
        tiredness_score = None
        distress_score = None
        sadness_score = None


        emotions = emoList[0]['results']['predictions'][0]['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']

        for emotion in emotions:
            if emotion['name'] == 'Anxiety':
                anxiety_score = emotion['score']
            elif emotion['name'] == 'Guilt':
                guilt_score = emotion['score']    
            elif emotion['name'] == 'Tiredness':
                tiredness_score = emotion['score']
            elif emotion['name'] == 'Distress':
                distress_score = emotion['score']
            elif emotion['name'] == 'Sadness':
                sadness_score = emotion['score']
        
        average = (anxiety_score + guilt_score + tiredness_score + anxiety_score + distress_score + sadness_score) / 5

        print("Anxiety Score:", anxiety_score)
        print("Guilt Score:", guilt_score)
        print("Tiredness Score:", tiredness_score)
        print("Anxiety Score:", anxiety_score)
        print("Distress Score:", distress_score)
        print("Sadness Score:", sadness_score)

        

        #trainable
        weights = {
            'Anxiety': 0.5,
            'Guilt': 0.15,
            'Tiredness': 0.15,
            'Distress': 0.15,
            'Sadness': 0.2
        }

        total_weight = sum(weights.values())

        weighted_average = (
            (weights['Anxiety'] * anxiety_score +
            weights['Guilt'] * guilt_score +
            weights['Tiredness'] * tiredness_score +
            weights['Distress'] * distress_score +
            weights['Sadness'] * sadness_score) / total_weight
        )

        output = { "Anxiety Score:": anxiety_score,
            "Guilt Score:": guilt_score,
            "Tiredness Score:": tiredness_score,
            "Anxiety Score:":  anxiety_score,
            "Distress Score:": distress_score,
            "Sadness Score:": sadness_score,
            "Weighted Average" :weighted_average
        }
        return output

    except requests.RequestException:
        return None


def create_signed_url(object_file):
    # Your Google Cloud Storage information
    bucket_name = "calhacks2023"
    object_name = object_file
    google_cloud_credentials_file = "GOOGLE_APPLICATION_CREDENTIALS.json"
    # Create a client using your Google Cloud credentials
    client = storage.Client.from_service_account_json(google_cloud_credentials_file)
    # Get a reference to the bucket
    bucket = client.get_bucket(bucket_name)
    # Get a reference to the object
    blob = bucket.blob(object_name)
    # Set the expiration time for the signed URL
    expiration = datetime.utcnow() + timedelta(hours=1)  # Adjust the expiration time as needed
    # Generate the signed URL
    signed_url = blob.generate_signed_url(
        expiration=expiration,
        method='GET'
    )
    print("Signed URL:", signed_url)

    return signed_url

