import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_request(url, **kwargs):
    response = None
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={
                'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except Exception as e:
        print("Error ", e)
    if response is not None:
        json_data = json.loads(response.text)
        return json_data
    else:
        return None


def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except:
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_from_cf_by_id(url, dealer_id):
    json_result = get_request(url, dealerId=dealer_id)

    print('json_result',json_result,dealer_id,url,'==============')

    if json_result and len(json_result) > 0:
        dealer = json_result[0]
        dealer_obj = CarDealer(address=dealer["address"],
                               city=dealer["city"],
                               full_name=dealer["full_name"],
                               id=dealer["id"],
                               lat=dealer["lat"],
                               long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"],
                               zip=dealer["zip"])
        return dealer_obj


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    if id:
        json_result = get_request(url, dealerId=dealer_id)
    else:
        json_result = get_request(url)
    if json_result:
        reviews = json_result["body"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                      name=dealer_review["name"],
                                      purchase=dealer_review["purchase"],
                                      review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]

            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


def analyze_review_sentiments(text):
    try:
        api_key = "JCsyaQJ3joXkfLb7Tl2GjNhPsAenEFeLTLRyH57Jghz1"
        url = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/9d827cd4-21e2-4619-9315-2ceb724fd73c'
        authenticator = IAMAuthenticator(api_key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2023-04-07',
            authenticator=authenticator
        )
        natural_language_understanding.set_service_url(url)
        target = 'here is what I want to say: ' + text + ' ' + text + ' ' + text
        response = natural_language_understanding.analyze(
            text=target,
            features=Features(sentiment=SentimentOptions(targets=[target]))).get_result()
        label = response['sentiment']['targets'][0]['label']
        return label
    except Exception as e:
        print("Error ", e)
        return 'normal'
