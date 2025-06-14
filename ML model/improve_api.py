from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field,computed_field
from typing import Literal ,Annotated
import pickle 
import pandas as pd 

# improvement
from pydantic import field_validator 

# import the model
with open("ML model/model.pkl",'rb') as f :
    
    model = pickle.load(f)
    
# improvement 4
MODEL_VERSION = '1.0.0'    
   
    
    
app =FastAPI()    
    
# Name of the city for the city_tier endpoint    
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
        
    
    
#pydantic model to validate  incoming data

class UserInput(BaseModel):
    age :Annotated[int,Field(...,gt =0 ,lt=120 ,description="Age of the User")]
    weight: Annotated[float,Field(...,gt =0 ,description="Weight of the User in kgs")]
    height:Annotated[float,Field(...,gt =0 ,lt=2.5 ,description="Height of the User in ms")]
    smoker:Annotated[bool,Field(...,description="Is the user is smoker")]
    city:Annotated[str,Field(...,description="The city of the user which he/she belongs to")]
    occupation:  Annotated[Literal['retired','freelancer','student','government_job' ,'bussiness_owner','unemployed','private_job'] ,Field(...,description="Occupation of the User")]  
    income_lpa:Annotated[float,Field(...,description="Annual salary of the user in lpa")]  
    
    # field validator for city --> improvement 1
    @field_validator('city')
    @classmethod
    def normalize_city(cls,v:str) ->str:
        v=v.strip().title() # if any whitespace before or after the name od city then strip and convert to title case -->M or m same
        return v
     
    # self BMI calculation
     
    @computed_field
    @property

    def bmi(self) ->float:
      bmi = self.weight /(self.height **2)   
      return bmi
  

    # lifestyle_risk of the user     
    @computed_field
    @property
    def lifestyle_risk(self) ->str:
        if self.smoker and self.bmi > 30:
          return "high"
        elif self.smoker and self.bmi  > 27:
          return "medium"
        else:
          return "low" 
      
    # City of the User
    @computed_field
    @property
    def city_tier(self) ->int:
       if self.city in tier_1_cities:
        return 1
       elif self.city in tier_2_cities:
        return 2
       else:
        return 3
    
    
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    


# Home url --> improvement 2
# human readable
@app.get("/")
def home():
    return {'message':'insurance prediction API'}

# for aws -> improvement 3
# machine readable 
@app.get('/health')
def health_check():     # other can be add -> 1. MODEL VERSION   extract from Mlops , 2.last api used  
     
    return {
        'status':'OK',
        'version':MODEL_VERSION,
        'model_loaded':model is not None
        
    }



# prediction
@app.post('/predict')
def predict(data:UserInput):
    input_df=pd.DataFrame([{
       'bmi': data.bmi
        ,'age_group':data.age_group
        ,'lifestyle_risk': data.lifestyle_risk
        ,'city_tier':data.city_tier
        ,'income_lpa':data.income_lpa
        ,'occupation':data.occupation
        
    }])
    
    # insurance_premium_category prediction -->['High', 'Low', 'Medium']
    try:
    # Predict the insurance premium category
      prediction = model.predict(input_df)[0]

    # Get the probabilities for each class (e.g., Low, Medium, High)
      probs = model.predict_proba(input_df)[0]


    # Return the prediction, model confidence, and all class probabilities
      return JSONResponse(status_code=200,
        content={"predicted_category": prediction,
                
            }    )

    except Exception as e:
    # If any error occurs during prediction, return HTTP 500 with error message
      return JSONResponse(status_code=500, content={"error": str(e)})
   
    
    
    
    
    
    
       
        
        
            

    