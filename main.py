# Importing necessary modules from FastAPI
from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
# For reading the JSON data
import json

# Pydantic for request data validation and computed fields
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

# Creating a FastAPI app instance
app = FastAPI()


# -------------------- Pydantic Model for Patient --------------------
class Patient(BaseModel):
    # Defining all required patient attributes using type hints and Field annotations
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]

    # Computed field for BMI auto calculated  
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    # Computed field for health verdict based on BMI
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
     
     
    # for the Put endpoint class is inherited     
class  PatientUpdate(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient lives")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age must be between 1 and 119")]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]

           


# -------------------- Helper Function --------------------
# Load data from JSON file
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

# save the data of POST request body
def save_data(data):
    with open('patients.json','w') as f:
        new_data= json.dump(data,f)
        return new_data
            


# -------------------- Routes --------------------

# Basic root endpoint
@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}


# About the API
@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records with health insights"}


# Endpoint to view all patient data
@app.get("/view")
def view():
    data = load_data()
    return data


# Endpoint to get a single patient by ID (Path Parameter)
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient in the DB", examples={"example": "P001"})
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


# Endpoint to sort patient data based on height, weight, or BMI (Query Parameters)
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description='Sort based on height, weight, or bmi'),
    order: str = Query('asc', description='Order to sort the data (asc or desc)')
):
    valid_fields = ['height', 'weight', 'bmi']

    # Validate sort_by field
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid field. Choose from {valid_fields}')

    # Validate sort order
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Choose asc or desc')

    data = load_data()

    # Define sorting order
    sort_order = True if order == 'desc' else False

    # Sort data using lambda
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


# Endpoint for the POST request body
# creating new patient
@app.post('/create')
def create_patient(patient:Patient):  # (variable: data_type)
                                      # patient contain all the validated data
    # load existing data
    data =load_data
    
    # check if the patient already existed
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    
    # new patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])  # convert the pydantic object to dict
    
    # save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201 ,content={'message':'patient created succesfully'})
    

# FOR updating the Patient PUT Endpoint usecase

@app.put("/edit/{patient_id}")  

def update_patient(patient_id:str, patientupdate: PatientUpdate):
      
    data =load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    existing_patient_info =data[patient_id]  # in the form dictionary
    
    update_patient_info=patientupdate.model_dump(exclude_unset=True)  # convert from str to dict ---> patientupdate: PatientUpdate
    
    for key ,value in update_patient_info.items:
        existing_patient_info[key] =value   # updating the city and weight 
        
    
   # existing_patient_info --> pydantic object --> updated_bmi + verdict--> 
   
    existing_patient_info['id']= patient_id # as there is no patient id so created new one
    patient_pydantic_obj =Patient(**existing_patient_info)  # pydantic object 
    #pydantic object -->dict
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id') # as there is already ID present
    
    
    # add this to data
    data[patient_id]= existing_patient_info
    
    # save data
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient updated'})     

# DELETE Endpoint
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    # load data
    data =load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404 ,detial ='Patient not found')
    
    del data[patient_id]   # deleting the patient
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'Patient Deleted'})
        