from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

#--------------------------------------------------------------------------

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(225), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name, date, description):
        self.name = name
        self.date = date
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.isoformat(),
            'description': self.description
        }

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    competition = db.relationship('Competition', backref=db.backref('result'))

    def __init__(self, competition_id, student_name, score):
        self.competition_id = competition_id
        self.student_name = student_name
        self.score = score

    def get_json(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'student_name': self.student_name,
            'score': self.score
        }


#--------------------------------------------------------------------------
