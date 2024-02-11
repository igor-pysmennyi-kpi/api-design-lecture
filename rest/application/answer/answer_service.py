import uuid

from application.answer.model.dto.answer import Answer
from application.answer.model.mapper.answer_mapper import AnswerMapper
from application.answer.model.dto.answer import Answer, db
from application.models import Page


class AnswerFilters:
    def __init__(self, author_id, question_id):
        self.author_id = author_id
        self.question_id = question_id

class AnswerService:
    def __init__(self):
        self.answer_mapper = AnswerMapper()
    
    def create_answer(self, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)

        answer_db = Answer(**answer)
        db.session.add(answer_db)
        db.session.commit()
        #маписо в ентітю і берігаємо в базу
        #return questions_mapper.map_entity_to_dto(question)
        return answer
    
    def update_answer(self, answer_id, request_data) -> Answer:
        answer = self.answer_mapper.map_request(request_data)
        #тут ще перед мапінгом в ентітю вигрібаємо з бази по айді і мапимо в існуючу, а не нову
        answer_db = Answer.query.get(answer_id)
        if answer_db:
            db.session.add(**answer)
            db.session.commit()
            #тут ще перед мапінгом в ентітю вигрібаємо з бази по айді і мапимо в існуючу, а не нову
            return answer

        return None
    
    def get_answer(self, answer_id) -> Answer:
        #витягли з бази і замаппали в дто
        answer_db = Answer.query.get(answer_id)
        return answer_db.serialize()
    
    def get_answers(self, filters: AnswerFilters, page: int, size: int) -> Page[Answer]:
        answers = [a.serialize() for a in Answer.query.all()]
        return Page(size=size, page=page, total_pages=1, content=answers)

