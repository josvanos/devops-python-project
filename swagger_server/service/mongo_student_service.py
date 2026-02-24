import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query
from bson.objectid import ObjectId
import pymongo

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = db_client["mydatabase"]


def add(student=None):
    existing_student = db['students'].find_one({
        "first_name": student.first_name,
        "last_name": student.last_name
    })

    if existing_student:
        return 'already exists', 409

    result = db['students'].insert_one(student.to_dict())
    student.student_id = str(result.inserted_id)
    return student.student_id

def get_by_id(student_id=None, subject=None):
    student = db['students'].find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    student['student_id'] = str(student['_id'])
    del student['_id']
    print(student)
    return student


def delete(student_id=None):
    student = db['students'].find_one({"_id": ObjectId(student_id)})
    if not student:
        return 'not found', 404

    result = db['students'].delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count == 0:
        return 'not found', 404

    return str(student['_id'])