from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models import Student

def get_student(session: Session, student_id: int) -> Student:
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

def get_students(session: Session):
    statement = select(Student)
    return session.exec(statement).all()

def create_student(session: Session, student: Student) -> Student:
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def update_student(session: Session, student_id: int, student_data: Student) -> Student:
    student = get_student(session, student_id)
    student.name = student_data.name
    student.age = student_data.age
    student.email = student_data.email
    student.grades = student_data.grades
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def delete_student(session: Session, student_id: int):
    student = get_student(session, student_id)
    session.delete(student)
    session.commit()
