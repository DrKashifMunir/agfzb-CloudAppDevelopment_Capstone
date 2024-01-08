import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def post_request(url, json_payload, **kwargs):
    print("POST from {} ".format(url))
    data = json_payload['review']
    response = requests.post(url, json=data)

    # Checking the response
    if response.status_code == 200:
        print("POST request was successful!")
        print("Response:", response.json())
    else:
        print("POST request failed with status code:", response.status_code)
        print("Response:", response.text)
    json_data = json.loads(response.text)
    return json_data

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #print(json_result)
        #dealers = json_result["rows"]
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url,dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    #dealer_id = kwargs.get('dealer_id')
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer_doc in dealers:
            if dealer_id ==  dealer_doc.get("dealership"):  
                print(dealer_doc)
                dealer_review_obj = DealerReview(
                    id=dealer_doc.get("id", ""),
                    name=dealer_doc.get("name", ""),
                    dealership=dealer_doc.get("dealership", ""),
                    review=dealer_doc.get("review", ""),
                    purchase=dealer_doc.get("purchase", ""),
                    purchase_date=dealer_doc.get("purchase_date", ""),
                    car_make=dealer_doc.get("car_make", ""),
                    car_model=dealer_doc.get("car_model", ""),
                    car_year=dealer_doc.get("car_year", ""),
                    sentiment=analyze_review_sentiments(dealer_doc.get("review"))
                )
                results.append(dealer_review_obj)

    return results

def analyze_review_sentiments(dealerreview):

    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/db7ddfa4-a0ad-42f1-ae80-fed8e799e08f/v1/analyze?version=2022-04-07"
    api_key = ""
    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "text": "Categorize the following text as positive, negative, or neutral: " + dealerreview,
        "features": {
         "sentiment": {}
        }
    }

    response = requests.post(url, auth=("apikey", api_key), headers=headers, json=data)

    print(response.status_code)
    sentiment = response.json()
    print(sentiment)

    print(sentiment['sentiment']['document']['label'])

    return sentiment['sentiment']['document']['label']

