from flask import Flask
from flask_migrate import Migrate

from application.question.questions_service import QuestionsService
from application.answer.answer_service import AnswerService
from application.models import db
from application.answer.answer_controller import answer_bp
from application.question.questions_controller import questions_bp


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(answer_bp)
app.register_blueprint(questions_bp)

# questions_service  = QuestionsService()
# answers_service = AnswerService()

# import application.question.questions_controller
# import application.answer.answer_controller
