from fastapi  import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

class Student(BaseModel):
    rollno: int
    name: str
    course: str

app = FastAPI()

students = {
    1 : {
        "rollno" : 123,
        "name" : "John",
        "course" : "cse"
    },
    2 : {
    "rollno" : 124,
    "name" : "Jane",
    "course" : "ece"
    }
}

@app.get("/students")
def get_students():
    return list(students.values())

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Invalid student ID")

    return students[student_id]

@app.post("/students")
def create_student(student: Student):
    new_id = max(students.keys(),default=0) + 1
    student_record = {
        **student.model_dump(),
    }
    students[new_id] = student_record
    return student_record

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Invalid student ID")

    students[student_id] = {
        **student.model_dump(),
    }
    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Invalid student ID")

    del students[student_id]
    return {"message": "Student deleted successfully"}

MONGO_URL = "mongodb://localhost:27017/"
client=MongoClient(MONGO_URL)
db=client["MyDB"]
student_collection = db["student"]
@app.get("/students")
def all_students():
    students=list(student_collection.find({},{"_id":0}))
    return students;

