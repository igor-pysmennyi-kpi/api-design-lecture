from flask import request, jsonify
from flask import Blueprint

from application.answer.answer_service import AnswerFilters, AnswerService

answer_bp = Blueprint('answer_bp', __name__)
answers_service = AnswerService()


# /questions/<question_id>/answers - давайте обговоримо за і проти такої архітектури
@answer_bp.route('/answers', methods=['POST'])
def create_answer():
    request_data = request.json
    answer = answers_service.create_answer(request_data)

    return jsonify(answer), 201

@answer_bp.route('/answers', methods=['GET'])
def get_answers():
    author_id = request.args.get('author_id')
    question_id = request.args.get('question_id')
    page = request.args.get('page')
    size = request.args.get('size')

    answers = answers_service.get_answers(AnswerFilters(author_id,question_id), page, size)
    answers.print_content()
    return jsonify(answers.to_json()), 200


@answer_bp.route('/answers/<answer_id>', methods=['GET'])
def get_answer(answer_id):
    answer = answers_service.get_answer(answer_id)
    if answer is None:
        return jsonify({'error': 'Answer not found'}), 404
    return jsonify(answer), 200

@answer_bp.route('/answers/<answer_id>', methods=['PUT'])
def update_answer(answer_id):
    request_data = request.json
    answer = answers_service.update_answer(answer_id, request_data)
    if answer is None:
        return jsonify({'error': 'Answer not found'}), 404
    return jsonify(answer), 200

# Питання з *** - як реалізуємо апвоут?