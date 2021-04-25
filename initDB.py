from main import app
from models import db, Exercise
import csv

db.create_all(app=app)

# # add code to parse csv, create and save exercise objects

with open('exercises.csv', mode='r') as csv_file:
    exerciseFile = csv.DictReader(csv_file)
    for exercise in exerciseFile:
        exercises = Exercise(id = exercise['id'],name=exercise['exercise_name'],
                            video_url=exercise['video_url'],
                            target_area=exercise['target_area']  
        )
        print(exercises)
        db.session.add(exercises)
    db.session.commit()

print('database initialized!')