from fastapi import APIRouter,HTTPException,status
from config import DRUG_SERVICE_URL
from pydantic import BaseModel
import mysql.connector
from config import DB_USER, DB_PASSWORD, DB_DATABASE, DB_HOST
import re
import os
import csv
import random
import pandas as pd
from config import STATIC_URL


select_query_by_id = "select * from drugs where id = %s"
select_query_all = "select * from drugs"



def id_to_index(input_id, data_frame):
    matching_row = data_frame.loc[data_frame['id'] == input_id]
    if not matching_row.empty:
      input_index = matching_row['index'].values[0]
      return input_index
    return None



def index_to_id(input_index, data_frame):
    matching_row = data_frame.loc[data_frame['index'] == input_index]
    if not matching_row.empty:
        input_id = matching_row['id'].values[0]
        return input_id
    
    return None

def read_csv_to_dict(csv_file):
    data = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            class_value = int(row['class'])
            drugs = list(map(int, row['drugs'].split(',')))
            data[class_value] = drugs
    
    return data

def find_drugs_in_class(data, drug_id):
    for class_value, drugs in data.items():
        if drug_id in drugs:
            return drugs
    return None

class RecommendationPayload(BaseModel):
   id : str

recommendationRoute = APIRouter()

responsePayload = {
    "service" : "recommendation service", 
    "status" : "success", 
    "request" : None, 
    "response" : {
        "data" : None,
        "total" : None,
        "recommendation" : None
    },
    "message" : None
}

@recommendationRoute.post('/api/recommendation')
def recommendation(request : RecommendationPayload):
    responsePayload["request"] = request

    ctx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                              host=DB_HOST,
                              database=DB_DATABASE)
    cursor = ctx.cursor()
    cursor.execute(select_query_all)
    columns_drugs = cursor.description
    drugs = [{columns_drugs[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    data_frame = pd.DataFrame(drugs)
    data_frame.reset_index(inplace=True)

    cursor.execute(select_query_by_id, [request.id])
    columns_drug = cursor.description 

    drug = [{columns_drug[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    if(len(drug) > 0):
        drug[0]["title"] = re.split("[\d.]", drug[0]['title'])[0]
    
    cursor.close()
    ctx.close()   

    if(len(drug) < 1):
        responsePayload['response']['data']= None
        responsePayload['status']= "error"
        responsePayload['message']= "drug not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=responsePayload)


    input_drugs = id_to_index(request.id,data_frame)

    if(input_drugs is None):
        responsePayload['response']['data']= None
        responsePayload['status']= "error"
        responsePayload['message']= "No matching row found for input ID"

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=responsePayload)

    
    df_cosine = pd.read_csv(f'{STATIC_URL}/cosine_similarity_table.csv')
    df_drug_per_class = read_csv_to_dict("assets/drugs_per_class.csv")
    drugs_in_class = find_drugs_in_class(df_drug_per_class, input_drugs)

    if drugs_in_class is None:
        responsePayload['response']['data']= None
        responsePayload['status']= "error"
        responsePayload['message']= "No class contains drug"

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=responsePayload)

    cosine_similarity = df_cosine.values
    
    threshold = 0.1 
    similarities = []
    data_kirim = []

    similar_obat = list(enumerate(drugs_in_class))
    for index, drug_value in similar_obat:
        similarity = cosine_similarity[input_drugs, drug_value]  
        similarities.append((similarity, drug_value))

    similarities.sort(reverse=True)
    similarities = similarities[1:]
    counter = 0
    for similarity, drug_value in similarities:
        if(similarity <= threshold):
            continue
        matching_rows = data_frame[data_frame['index'] == drug_value]
        response = matching_rows.drop(columns=["index"])
        data_kirim.append(response.to_dict("records")[0])
        counter += 1
        if counter >= 6:
            break

    if len(data_kirim) > 0:
        for recommended_drug in data_kirim:
            recommended_drug["title"] = re.split("[\d.]", recommended_drug['title'])[0]
    
    responsePayload['status']= "success"
    responsePayload['message']= "recommendation service success get drug"
    responsePayload['response']['data'] = drug[0] if len(drug) > 0 else None
    responsePayload['response']['recommendation'] = data_kirim if len(data_kirim) > 0 else None
    return responsePayload