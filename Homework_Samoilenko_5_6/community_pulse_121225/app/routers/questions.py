from flask import Blueprint, request, jsonify, abort
from pydantic import ValidationError

from app.models import db, Question

from app.schemas.questions import QuestionCreate, QuestionUpdate
from app.schemas.statistics import StatisticsRead

from app.contracts import *


questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/', methods=['GET', 'POST'])
def questions():
    if request.method == "GET":
        items = Question.query.all()
        result = QuestionListResponse(
            items=[QuestionResponse.model_validate(item) for item in items],
            count=len(items),
        )
        return jsonify(result.model_dump()), 200
    if request.method == "POST":
        try:
            raw = request.get_json(silent=False)
        except Exception as e:
            return jsonify(ErrorResponse(error="JSON is not valid").model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error="No data").model_dump()), 400

        try:
            data = QuestionCreate.model_validate(raw)
            question = Question(**data.model_dump())
            db.session.add(question)
            db.session.commit()

            return jsonify(QuestionResponse.model_validate(question).model_dump()), 201

        except ValidationError as e:
            return jsonify(ErrorResponse(error="Data is not valid").model_dump()), 400




@questions_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def question(id):
    question = db.session.get(Question, id)
    if not question:
        return jsonify(ErrorResponse(error=f"Question not found with id={id}").model_dump()), 404

    if request.method == "GET":

        stats = StatisticsRead.model_validate(question.statistics) if question.statistics else None
        result = QuestionDetailResponse(
            id=question.id,
            text=question.text,
            statistics=stats
        )
        return jsonify(result.model_dump(exclude_none=True)), 200
    if request.method == "PUT":
        try:
            raw = request.get_json(silent=False)
        except Exception as e:
            return jsonify(ErrorResponse(error="JSON is not valid").model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error="No data").model_dump()), 400

        try:
            data = QuestionUpdate.model_validate(raw)
            question.text = data.text
            db.session.commit()

            return jsonify(QuestionResponse.model_validate(question).model_dump()), 200
        except ValidationError as e:
            return jsonify(ErrorResponse(error="Data is not valid").model_dump()), 400

    if request.method == "DELETE":
        # try
        db.session.delete(question)
        db.session.commit()
        return '', 204