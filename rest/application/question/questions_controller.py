from flask import request, jsonify
from flask import Blueprint

from application.question.questions_service import QuestionFilters, QuestionsService


questions_bp = Blueprint('questions_bp', __name__)
questions_service = QuestionsService()

@questions_bp.route('/questions', methods=['POST'])
def create_question():

    request_data = request.json
    question = questions_service.create_question(request_data)
    return jsonify(question), 201

@questions_bp.route('/questions', methods=['GET'])
def get_questions():
    author_id = request.args.get('author_id')
    page = request.args.get('page')
    size = request.args.get('size')

    questions = questions_service.get_questions(QuestionFilters(author_id), page, size)
    questions.print_content()
    return jsonify(questions.to_json()), 200


@questions_bp.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    question = questions_service.get_question(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question), 200

@questions_bp.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    request_data = request.json
    question = questions_service.update_question(question_id, request_data)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify(question), 200

# @app.route('/questions/<question_id>', methods=['DELETE'])
# def delete_question(question_id):
# а в розподілених системах нема делівтів (тільки для тестів). Давайте поговоримо чому так