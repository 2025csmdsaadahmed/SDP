from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# Connect to MongoDB
MONGO_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URL)

# Database
db = client["MyDB"]

# Collection
student_collection = db["student"]


# Student model
class Student(BaseModel):
    rollno: int
    name: str
    course: str


# GET ALL STUDENTS
@app.get("/students")
def get_all_students():

    students = list(
        student_collection.find({}, {"_id": 0})
    )

    return students


# GET STUDENT BY ROLL NUMBER
@app.get("/student/{student_id}")
def get_student_by_id(student_id: int):

    student = student_collection.find_one(
        {"Rollno": student_id},
        {"_id": 0}
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="No Record ID"
        )

    return student


# POST - INSERT NEW STUDENT
@app.post("/student")
def insert_record(student: Student):

    student_record = {
        "Rollno": student.rollno,
        "Name": student.name,
        "Course": student.course
    }

    student_collection.insert_one(student_record)

    return {
        "message": "Record inserted successfully",
        "data": student_record
    }
@app.put("/student/{student_id}")
def update_record(student_id:int, student:Student):
    result = student_collection.update_one({"rollno":student_id},{"$set":student.model_dump()})

    if result is None:
        raise HTTPException(status_code=404 , detail="Invalid Student ID")
        return "Record Updated Successfully"
    
@app.delete("/student/{student_id}")
def delete_record(student_id:int):
    result = student_collection.delete_one({"rollno":student_id})
    if result is None:
        raise HTTPException(status_code=404 , detail="Invalid Student ID")

    return "Record deleted Successfully"
    
