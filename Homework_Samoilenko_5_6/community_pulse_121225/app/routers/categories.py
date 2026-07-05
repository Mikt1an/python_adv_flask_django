from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from app.models import db, Category
from app.contracts import (ErrorResponse,
                            CategoryCreateRequest,
                            CategoryUpdateRequest,
                            CategoryResponse,
                            CategoryListResponse,
                            )


categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/", methods=["GET", "POST"])
def categories():
    if request.method == "GET":
        items = Category.query.all()

        result = CategoryListResponse(
            items=[CategoryResponse.model_validate(item) for item in items],
            count=len(items),
        )

        return jsonify(result.model_dump()), 200

    if request.method == "POST":
        try:
            raw = request.get_json(silent=False)
        except Exception:
            return jsonify(ErrorResponse(error="JSON is not valid").model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error="No data").model_dump()), 400

        try:
            data = CategoryCreateRequest.model_validate(raw)

            category = Category(**data.model_dump())

            db.session.add(category)
            db.session.commit()

            return jsonify(CategoryResponse.model_validate(category).model_dump()), 201

        except ValidationError:
            return jsonify(ErrorResponse(error="Data is not valid").model_dump()), 400


@categories_bp.route("/<int:id>", methods=["PUT", "DELETE"])
def category(id):
    category = db.session.get(Category, id)

    if not category:
        return jsonify(ErrorResponse(error=f"Category not found with id={id}").model_dump()), 404

    if request.method == "PUT":
        try:
            raw = request.get_json(silent=False)
        except Exception:
            return jsonify(ErrorResponse(error="JSON is not valid").model_dump()), 400

        if not raw:
            return jsonify(ErrorResponse(error="No data").model_dump()), 400

        try:
            data = CategoryUpdateRequest.model_validate(raw)

            if data.name is not None:
                category.name = data.name

            db.session.commit()

            return jsonify(CategoryResponse.model_validate(category).model_dump()), 200

        except ValidationError:
            return jsonify(ErrorResponse(error="Data is not valid").model_dump()), 400

    if request.method == "DELETE":
        db.session.delete(category)
        db.session.commit()

        return "", 204