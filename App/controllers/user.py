from App.models import User, Competition, Result
from App.database import db
#-------
import os
import csv
import datetime
#-------

# user functions
def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
#-------------------------------------------

# competition functoins

def create_competition(name, date_str, description):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    new_competition = Competition(name=name, date=date, description=description)
    db.session.add(new_competition)
    db.session.commit()
    return new_competition

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()
    if not competitions:
        return []
    competitions = [competition.get_json() for competition in competitions]
    return competitions

def get_competition_by_id(competition_id):
    return Competition.query.get(competition_id)


# results functions

def create_result(competition_id, student_name, score):
    new_result = Result(competition_id=competition_id, student_name=student_name, score=score)
    db.session.add(new_result)
    db.session.commit()
    return new_result

def get_all_results():
    return Result.query.all()

def get_all_results_json():
    results = Result.query.all()
    if not results:
        return []
    results = [result.get_json() for result in results]
    return results

def get_results_by_competition(competition_id):
    return Result.query.filter_by(competition_id=competition_id).all()

def import_competitions_result_from_file(file_path):
    file_abs_path = os.path.join('data', file_path)

    try:
        with open(file_abs_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                competition_id = int(row['competition_id'])
                student_name = row['student_name']
                score = int(row['score'])

                new_result = Result(
                    competition_id=competition_id,
                    student_name=student_name,
                    score=score
                )

                db.session.add(new_result)

            db.session.commit()
            print(f"Results imported from {file_path}")
    
    except FileNotFoundError:
        print(f"File not found")
    
    except Exception as e:
        print(f"Error: {e}")


#-------------------------------------------