from math import ceil

from application.question.model.dto.question import Question
from application.question.model.mapper.question_mapper import QuestionMapper
from application.models import Page
from application.db import connect

class QuestionFilters:
    def __init__(self, author_id):
        self.author_id = author_id

class QuestionsService:
    def __init__(self):
        self.questions_mapper = QuestionMapper()

    def create_question(self, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        con = connect()
        cur = con.cursor()
        cur.execute('INSERT INTO questions (author_id, body) VALUES (%s, %s);',
                    (question.author_id, question.body))
        con.commit()
        cur.close()
        con.close()
        return question

    def update_question(self, question_id, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        con = connect()
        cur = con.cursor()
        cur.execute('UPDATE questions SET author_id=%s, body=%s WHERE id = %s;',
                    (question.author_id, question.body, question_id))
        con.commit()
        cur.close()
        con.close()

        return question

    def get_question(self, question_id) -> Question:
        con = connect()
        cur = con.cursor()
        cur.execute('SELECT id, author_id, body FROM questions WHERE id = %s;', (question_id,))
        question = cur.fetchone()
        question = Question(id=question[0], author_id=question[1], body=question[2])
        cur.close()
        con.close()
        return question

    def get_questions(self, filters: QuestionFilters, page: int, size: int) -> Page[Question]:
        con = connect()
        cur = con.cursor()
        cur.execute(
            'SELECT id, author_id, body, COUNT(*) OVER () AS total_count FROM questions ORDER BY id OFFSET %s LIMIT %s;',
            ((page - 1) * size, size))
        questions = cur.fetchall()
        total_count = 0
        if len(questions) > 0:
            total_count = questions[0][3]
        questions = [Question(id=el[0], author_id=el[1], body=el[2]) for el in questions]

        cur.close()
        con.close()

        return Page(size=size, page=page, total_pages=ceil(total_count / size), content=questions)
