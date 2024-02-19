from application.models import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.VARCHAR(12), primary_key=True)
    author_id = db.Column(db.VARCHAR(12))
    body = db.Column(db.String(120))  

    @property
    def serialize(self):
        return {
            'id': Question.id,
            'author_id': Question.author_id,
            'body': Question.body,
        }
