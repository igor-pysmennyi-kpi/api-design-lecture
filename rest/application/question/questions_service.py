import uuid

from application.question.model.dto.question import Question
from application.question.model.mapper.question_mapper import QuestionMapper
from application.question.model.question_DB import QuestionDB
from application.models import Page

class QuestionFilters:
    def __init__(self, author_id):
        self.author_id = author_id

class QuestionsService:
    def __init__(self):
        self.questions_mapper = QuestionMapper()
        self.questionDB = QuestionDB()
    
    def create_question(self, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        self.questionDB.create_question(question)
        return question
    
    def update_question(self, question_id, request_data) -> Question:
        question = self.questions_mapper.map_request(request_data)
        self.questionDB.update_question(question_id, question)
        return question
    
    def get_question(self, question_id) -> Question:
        question_data = self.questionDB.get_question(question_id)
        if question_data:
            return Question(question_data['id'], question_data['author_id'], question_data['body'])
        return None
    
    def get_questions(self, filters: QuestionFilters, page: int, size: int) -> Page[Question]:
        questions = self.questionDB.list_questions()
        content = [Question(q['id'], q['author_id'], q['body']) for q in questions]
        return Page(size=size, page=page, total_pages=1, content=content)
