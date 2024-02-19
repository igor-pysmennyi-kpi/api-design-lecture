import uuid

from application.question.model.dto.question import Question
from application.question.model.mapper.question_mapper import QuestionMapper
from application.question.model.dto.question import Question, db
from application.models import Page

class QuestionFilters:
    def __init__(self, author_id):
        self.author_id = author_id

class QuestionsService:
    def __init__(self):
        self.questions_mapper = QuestionMapper()
    
    def create_question(self, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        #маписо в ентітю і берігаємо в базу
        #return questions_mapper.map_entity_to_dto(question)
        question_db = Question(**question)
        db.session.add(question_db)
        db.session.commit()

        return question_db
    
    def update_question(self, question_id, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        question_db = Question.query.get(question_id)
        if question_db:
            db.session.add(**question)
            db.session.commit()
            #тут ще перед мапінгом в ентітю вигрібаємо з бази по айді і мапимо в існуючу, а не нову
            return question
        return None
    
    def get_question(self, question_id) -> Question:
        #витягли з бази і замаппали в дто
        question_db = Question.query.get(question_id)
        return question_db.serialize()
    
    def get_questions(self, filters: QuestionFilters, page: int, size: int) -> Page[Question]:
        questions = [q.serialize() for q in Question.query.all()]
        return Page(size=size, page=page, total_pages=1, content=questions)
