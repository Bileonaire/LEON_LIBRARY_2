"""Contains all endpoints to manipulate history information
"""
import datetime

from flask import jsonify, Blueprint, make_response, request
from flask_restful import Resource, Api

import models
from .auth import admin_required
import config


class AllHistory(Resource):
    """Contains GET all history method"""


    @admin_required
    def get(self):
        """Gets all history"""
        result = models.History.get_all_history()
        return result


class BookHistory(Resource):
    """Contains GET all history method"""


    @admin_required
    def get(self, book_id):
        """Gets all history of a paricular book"""
        result = models.History.get_all_bookhistory(book_id)
        return result


class UserHistory(Resource):
    """Contains GET all history method"""


    @admin_required
    def get(self, user_id):
        """Gets all history of a paricular book"""
        result = models.History.get_all_userhistory(user_id)
        return result


history_api = Blueprint('resources.history', __name__)
api = Api(history_api) # create the API
api.add_resource(AllHistory, '/history', endpoint='history')
api.add_resource(BookHistory, '/bookhistory/<int:book_id>', endpoint='bookhistory')
api.add_resource(UserHistory, '/userhistory/<int:user_id>', endpoint='userhistory')
