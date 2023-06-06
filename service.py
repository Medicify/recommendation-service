from fastapi import APIRouter
import requests
from config import DRUG_SERVICE_URL
from pydantic import BaseModel
import mysql.connector
from config import DB_USER, DB_PASSWORD, DB_DATABASE, DB_HOST
import re

select_query = "select * from drugs where id = %s"
ctx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_DATABASE)


cursor = ctx.cursor()

class RecommendationPayload(BaseModel):
   id : str

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
    # drugs = requests.get(DRUG_SERVICE_URL)
    # drugs = drugs.json()["response"]["data"]
    # drug = requests.get(f"{DRUG_SERVICE_URL}?title={request.title}&category={request.drugType}")
    # drug = drug.json()['response']['data']

    cursor.execute(select_query, [request.id])
    columns = cursor.description 
    drug = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

    if(len(drug) > 0):
        drug[0]["title"] = re.split("[\d.]", drug[0]['title'])[0]


    responsePayload["request"] = request
    responsePayload['response']['data'] = drug[0] if len(drug) > 0 else None
    return responsePayload