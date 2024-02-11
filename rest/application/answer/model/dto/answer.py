from application.models import db


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.VARCHAR(12), primary_key=True)
    author_id = db.Column(db.VARCHAR(12))
    question_id = db.Column(db.VARCHAR(12))
    score = db.Column(db.Integer)  
    body = db.Column(db.String(120))  

    @property
    def serialize(self):
        return {
            'id': Answer.id,
            'author_id': Answer.author_id,
            'question_id': Answer.question_id,
            'score': Answer.score,
            'body': Answer.body,
        }
