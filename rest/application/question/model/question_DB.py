from tinydb import TinyDB, Query
import uuid
import os

class QuestionDB:
    def __init__(self):
        db_path = os.getenv('TINYDB_PATH')
        self.db = TinyDB(db_path)
        self.questions_table = self.db.table('questions')

    def create_question(self, question):
        question_dict = question.__dict__
        question_dict['id'] = str(question.id)
        question_dict['author_id'] = str(question.author_id)
        self.questions_table.insert(question_dict)
        return question

    def get_question(self, question_id):
        QuestionQuery = Query()
        result = self.questions_table.search(QuestionQuery.id == str(question_id))
        if result:
            data = result[0]
            return {'id': data['id'], 'author_id': data['author_id'], 'body': data['body']}
        return None

    def update_question(self, question_id, updated_data):
        QuestionQuery = Query()
        self.questions_table.update(updated_data.__dict__, QuestionQuery.id == str(question_id))

    def delete_question(self, question_id):
        QuestionQuery = Query()
        self.questions_table.remove(QuestionQuery.id == str(question_id))

    def list_questions(self):
        return [{'id': q['id'], 'author_id': q['author_id'], 'body': q['body']} for q in self.questions_table.all()]
