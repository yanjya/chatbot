from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel


app = FastAPI()

class Student(BaseModel):
    name: str
    age: int

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None

students= {
    1 :{
        'name' : 'aa',
        'age' : 23,

    },
    2 :{
        'name' : 'aaaa',
        'age' : 87,

    },
    3 :{
        'name' : 'haha',
        'age' : 11111,

    }

}


@app.get("/")
def greeting():
    return {"name": "data"}

@app.get("/student/{student_id}")
def get_student(student_id: int):
    return students[student_id]

@app.get("/get-by-name")
def get_student_name(name: str = None):
    for student_id in students:
        if students[student_id]['name'] == name:
            return students[student_id]
        # else:  
    return {"Data": "you "}

@app.post("/create-student/{student_id}")
def add_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return {"add student":students[student_id]}

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exists"}
    students[student_id] = student
    return {"update student":students[student_id]}
# @app.post("/create-student")
# def add_student(student: Student):

#   student.id = len(students) + 1

#   students.append(student)

#   return students[-1]
