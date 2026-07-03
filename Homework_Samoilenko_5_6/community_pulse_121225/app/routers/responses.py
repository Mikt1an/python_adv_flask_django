from flask import Blueprint, request


responses_bp = Blueprint('responses', __name__)


@responses_bp.route('/', methods=['GET', 'POST'])
def responses():
    if request.method == 'GET':
        return 'List of responses'
    if request.method == 'POST':
        return 'Add response'


@responses_bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_response(id):
    if request.method == 'GET':
        return f'Get response {id}'
    if request.method == 'PUT':
        return f'Put response {id}'
    if request.method == 'DELETE':
        return f'Delete response {id}'