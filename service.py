from fastapi import APIRouter
import requests
from config import DRUG_SERVICE_URL
from pydantic import BaseModel


class RecommendationPayload(BaseModel):
    title: str
    drugType : str

recommendationRoute = APIRouter()

responsePayload = {
    "service" : "recommendation service", 
    "status" : "success", 
    "request" : None, 
    "response" : {
        "data" : None,
        "total" : None
    }
}

@recommendationRoute.post('/api/recommendation')
def recommendation(request : RecommendationPayload):
    drugs = requests.get(DRUG_SERVICE_URL)
    drugs = drugs.json()["response"]["data"]
    drug = requests.get(f"{DRUG_SERVICE_URL}?title={request.title}&category={request.drugType}")
    drug = drug.json()['response']['data']

    responsePayload["request"] = request
    responsePayload['response']['data'] = drug
    return responsePayload