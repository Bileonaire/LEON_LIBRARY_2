"""Contains all endpoints to manipulate meal information
"""
import datetime

from flask import jsonify, Blueprint, make_response, request
from flask_restful import Resource, Api, reqparse, inputs
import jwt

import models
from .auth import token_required, admin_required
import config


class BookList(Resource):
    """Contains GET and POST methods"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=False,
            type=str,
            help="kindly provide a valid author's name",
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'copies',
            required=True,
            nullable=True,
            help="kindly provide a valid number of copies available",
            default=1,
            type=int,
            location=['form', 'json'])
        super().__init__()
    
    @admin_required
    def post(self):
        """Adds a new book"""
        kwargs = self.reqparse.parse_args()
        result = models.Book.create_book(book=kwargs.get('book'),
                                           author=kwargs.get('author'),
                                            copies=kwargs.get('copies'))
        return result

    def get(self):
        """Gets all books"""
        result = models.Book.get_all_books()
        return result


class Book(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single book"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book name',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=True,
            type=str,
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'copies',
            required=True,
            nullable=True,
            help="kindly provide a valid number of copies available",
            default=1,
            type=int,
            location=['form', 'json'])
        
        super().__init__()
    

    def get(self, book_id):
        """Get a particular book"""
        book = models.Book.get_book(book_id)
        return book

    @admin_required
    def put(self, book_id):
        """Update a particular book"""
        kwargs = self.reqparse.parse_args()
        result = models.Book.update_book(book_id=book_id,
                                         author=kwargs.get('author'),
                                         book=kwargs.get('book'),
                                         copies=kwargs.get('copies'))
        return result
    
    @admin_required
    def delete(self, book_id):
        """Delete a particular book"""
        result = models.Book.delete_book(book_id)
        return result

class BorrowedList(Resource):
    """Contains GET and POST methods for manipulating borrowed books data"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'borrowed_book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book to borrow',
            location=['form', 'json'])
        super().__init__()
    
    @token_required
    def post(self):
        """Adds a book to the borrowerd books"""
        kwargs = self.reqparse.parse_args()
        token = request.headers['x-access-token']
        data = jwt.decode(token, config.Config.SECRET_KEY)
        user_id = data['id']
        Borrowed_book = kwargs.get("borrowed_book")


        result = models.Borrowed.borrow_book(user_id=user_id,
                                            borrowed_book=Borrowed_book)
        return result


    def get(self):
        """Gets all borrowed books"""
        borrowed_books = models.Borrowed.get_all_borrowed()
        return borrowed_books


class Borrowed_book(Resource):
    """Contains GET, PUT and DELETE methods for manipulating a single borrowed book"""


    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'borrowed_book',
            required=True,
            type=inputs.regex(r"(.*\S.*)"),
            help='kindly provide a book to borrow',
            location=['form', 'json'])
        self.reqparse.add_argument(
            'author',
            required=True,
            type=str,
            default="author",
            location=['form', 'json'])
        self.reqparse.add_argument(
            'returned',
            required=False,
            nullable=True,
            default=False,
            type=bool,
            location=['form', 'json'])
        super().__init__()

    @token_required
    def get(self,borrowed_id):
        """Get a particular borrowed book"""
        borrowed = models.Borrowed.get_borrowed(borrowed_id)
        return borrowed
    
    @admin_required
    def put(self, borrowed_id):
        """returns a particular borrowed book"""
        result = models.Borrowed.return_borrowed(borrowed_id)
        return result


    @admin_required
    def delete(self, borrowed_id):
        """Delete a particular borrowed book"""
        result = models.Borrowed.delete_book(borrowed_id)
   
        return result


books_api = Blueprint('resources.books', __name__)
api = Api(books_api) # create the API
api.add_resource(BookList, '/books', endpoint='books')
api.add_resource(Book, '/books/<int:book_id>', endpoint='book')

api.add_resource(BorrowedList, '/borrowed', endpoint='borrowed')
api.add_resource(Borrowed_book, '/borrowed/<int:borrowed_id>', endpoint='borrowedbook')
