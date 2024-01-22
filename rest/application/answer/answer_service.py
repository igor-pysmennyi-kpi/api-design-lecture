from math import ceil

from application.answer.model.dto.answer import Answer
from application.answer.model.mapper.answer_mapper import AnswerMapper
from application.models import Page
from application.db import connect

class AnswerFilters:
    def __init__(self, author_id, question_id):
        self.author_id = author_id
        self.question_id = question_id

class AnswerService:
    def __init__(self):
        self.answer_mapper = AnswerMapper()
    
    def create_answer(self, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)
        con = connect()
        cur = con.cursor()
        cur.execute('INSERT INTO answers (author_id, question_id, score, body) VALUES (%s, %s, %s, %s);',
                    (answer.author_id, answer.question_id, 0, answer.body))
        con.commit()
        cur.close()
        con.close()
        return answer
    
    def update_answer(self, answer_id, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)
        con = connect()
        cur = con.cursor()
        cur.execute('UPDATE answers SET author_id=%s, question_id=%s, body=%s WHERE id = %s;',
                    (answer.author_id, answer.question_id, answer.body, answer_id))
        con.commit()
        cur.close()
        con.close()

        return answer
    
    def get_answer(self, answer_id) -> Answer:
        con = connect()
        cur = con.cursor()
        cur.execute('SELECT id, author_id, question_id, score, body FROM answers WHERE id = %s;', (answer_id,))
        answer = cur.fetchone()
        answer = Answer(id=answer[0], author_id=answer[1], question_id=answer[2], score=answer[3], body=answer[4])
        cur.close()
        con.close()
        return answer
    
    def get_answers(self, filters: AnswerFilters, page: int, size: int) -> Page[Answer]:
        con = connect()
        cur = con.cursor()
        cur.execute(
            'SELECT id, author_id, question_id, score, body, COUNT(*) OVER () AS total_count FROM answers ORDER BY id OFFSET %s LIMIT %s;',
                    ((page - 1) * size, size))
        answers = cur.fetchall()
        total_count = 0
        if len(answers) > 0:
            total_count = answers[0][5]
        answers = [Answer(id=el[0], author_id=el[1], question_id=el[2], score=el[3], body=el[4]) for el in answers]
        cur.close()
        con.close()
        return Page(size=size, page=page, total_pages=ceil(total_count / size), content=answers)
    
    def upvote(self, answer_id):
        con = connect()
        cur = con.cursor()
        cur.execute('UPDATE answers SET score=score+1 WHERE id = %s;', (answer_id,))
        con.commit()
        cur.close()
        con.close()

    def downvote(self, answer_id):
        con = connect()
        cur = con.cursor()
        cur.execute('UPDATE answers SET score=score-1 WHERE id = %s;', (answer_id,))
        con.commit()
        cur.close()
        con.close()
