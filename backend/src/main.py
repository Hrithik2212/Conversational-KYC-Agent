# main.py

from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.get("/getquestions")
async def getQuestions():
    try:
        questions=[{"label":"name","question":"What is your name?","speak":"Spell your name out if your name id raj spell it as R A J"},
                    {"label":"email","question":"What is your email?","speak":"Spell your name out if your name id raj spell it as R A J"},
                   ]
        return {"questions": questions}
    except:
        raise  HTTPException(status_code=400,detail="Invalid Mode type")