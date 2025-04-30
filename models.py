from flask_sqlalchemy import*
db=SQLAlchemy()
class User(db.model):
    id=db.column(db.integer,primary_key =True)
    username=db.column(db.String(90),unique=True,nllable=False)
    password=db.column(db.String(90),nullable=false)

class Candidate(db.model):
    id=db.column(db.Integer,primary_key=True)
    name=db.column(db.String(90),nullable=False)
class Vote(db.model):
    id=db.column(db.integer,primary_key=True)
    user_id=db.column(db.integer,df.ForeignKey('user.id'))
    candidate_id=db.column(db.integer,db.ForeignKey('candidate.id'))