"""Handles data storage for Users, books and borrowed books
"""
# pylint: disable=E1101
import datetime

from flask import make_response, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Contains user columns and methods to add, update and delete a user"""


    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean)
    borrowed = db.relationship("Borrowed", backref=db.backref('user'))
    
    def __repr__(self):
        return '<user {}>'.format(self.user)


    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """Creates a new user and ensures that the email is unique"""

        by_email = cls.query.filter_by(email=email).first()

        if by_email is None:
            password = generate_password_hash(password, method='sha256')
            new_user = cls(username=username, email=email, password=password, admin=admin)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({
                "message" : "user has been successfully created",
                str(new_user.id) : {"username" : new_user.username,
                                    "email" : new_user.email,
                                    "admin" : new_user.admin}}), 201)


        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def update_user(user_id, username, email, password, admin=False):
        """Updates user information"""
        user = User.query.get(user_id)
        by_email = User.query.filter_by(email=email).first()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        if by_email is None:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            user.admin = admin
            db.session.commit()
        
            borrowed = []
            borrowed_by = Borrowed.query.filter_by(user_id=user_id, returned=False).all()
            for each in borrowed_by:
                borrowed.append(each.book.book)

            return make_response(jsonify({
                "message" : "user has been successfully updated",
                str(user.id) : {"username" : user.username,
                                "email" : user.email,
                                "admin" : user.admin,
                                "borrowed" : borrowed}}), 200)

        return make_response(jsonify({"message" : "user with that email already exists"}), 400)


    @staticmethod
    def delete_user(user_id):
        """Deletes a user"""
        user = User.query.filter_by(id=user_id).first()
        has_book = Borrowed.query.filter_by(user_id=user_id).all()

        if user is None:
            return make_response(jsonify({"message" : "user does not exists"}), 404)

        db.session.delete(user)
        db.session.commit()
        if has_book != None:
            for book in has_book:
                db.session.delete(book)
            return make_response(jsonify({"message" : "The user has been deleted but had a borrowed book"}), 200)
        return make_response(jsonify({"message" : "user has been successfully deleted"}), 200)


    @staticmethod
    def get_user(user_id):
        """Gets a particular user"""
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return make_response(jsonify({"message" : "user does not exists"}), 404)
        
        borrowed = []
        borrowed_by = Borrowed.query.filter_by(user_id=user_id, returned=False).all()
        for each in borrowed_by:
            borrowed.append(each.book.book)

        info = {"user_id" : user.id, "email" : user.email,
                "username" : user.username, "admin" : user.admin,
                "borrowed" : borrowed}

        return make_response(jsonify(info), 200)
    
    @staticmethod
    def get_all_users():
        """Gets all users"""
        users = User.query.all()
        all_users = []
        for user in users:
        
            borrowed = []
            borrowed_by = Borrowed.query.filter_by(user_id=user.id, returned=False).all()
            for each in borrowed_by:
                borrowed.append(each.book.book)

            info = {user.id : {"email" : user.email,
                    "username" : user.username, "admin" : user.admin,
                    "borrowed" : borrowed}}
            all_users.append(info)

        return make_response(jsonify({"ALL USERS" : all_users}), 200)

class Book(db.Model):
    """Contains book columns and methods to add, update and delete a book"""
    

    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=True, default="author")
    copies = db.Column(db.Integer, nullable=False)
    borrowedbook = db.relationship("Borrowed", backref=db.backref('book', lazy=False))


    def __repr__(self):
        return '<book {}>'.format(self.book)


    @classmethod
    def create_book(cls, book, author, copies):
        """Creates a new book and ensures that the name is unique"""
        by_name = cls.query.filter_by(book=book).first()

        if by_name is None:
            new_book = cls(book=book, author=author, copies=copies)
            db.session.add(new_book)
            db.session.commit()
            return make_response(jsonify({
                "message" : "book has been successfully created",
                str(new_book.id) : {"book" : new_book.book,
                                    "author" : new_book.author,
                                    "copies" : new_book.copies}}), 201)

        return make_response(jsonify({"message" : "book with that name already exists"}), 400)


    @staticmethod
    def update_book(book_id, book, author, copies):
        """Updates book information"""
        updatebook = Book.query.filter_by(id=book_id).first()
        by_name = Book.query.filter_by(book=book).first()

        if updatebook is None:
            return make_response(jsonify({"message" : "book does not exists"}), 404)

        if by_name is None:
            updatebook.book = book
            updatebook.author = author
            updatebook.copies = copies

            db.session.commit()
            return make_response(jsonify({
                "message" : "book has been successfully updated",
                str(updatebook.id) : {"book" : updatebook.book,
                                "author" : updatebook.author,
                                 "copies" : updatebook.copies}}), 200)

        return make_response(jsonify({"message" : "book with that name already exists"}), 400)


    @staticmethod
    def delete_book(book_id):
        """Deletes a book"""
        book = Book.query.filter_by(id=book_id).first()

        if book is None:
            return make_response(jsonify({"message" : "book does not exists"}), 404)

        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({"message" : "book has been successfully deleted"}), 200)


    @staticmethod
    def get_book(book_id):
        """Gets a particular book"""
        book = Book.query.get(book_id)

        if book is None:
            return make_response(jsonify({"message" : "book does not exists"}), 404)
        
        borrowed = []
        borrowed_by = Borrowed.query.filter_by(book_id=book_id, returned=False).all()
        for each in borrowed_by:
            borrowed.append(each.user.username)

        info = {"book" : book.book, "author" : book.author, "copies" : book.copies,
                "borrowed by" : borrowed}
        return make_response(jsonify({book.id : info}), 200)
    
    @staticmethod
    def get_all_books():
        """Gets all books"""
        books = Book.query.all()
        get_all = []

        for book in books:
        
            borrowed = []
            borrowed_by = Borrowed.query.filter_by(borrowed_book=book.book, returned=False).all()
            for each in borrowed_by:
                borrowed.append(each.user.username)

            info = {book.id : {"book" : book.book, "author" : book.author, "copies" : book.copies,
                    "borrowed by" : borrowed}}
            get_all.append(info)

        return make_response(jsonify({"All Books" : get_all}), 200)


class Borrowed(db.Model):
    """Contains menu columns and methods to add, update and delete a menu option"""
   
    __tablename__ = 'borrowed'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=True)
    borrowed_book = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=True)
    returned = db.Column(db.Boolean)
        
    def __repr__(self):
        return '<borrowed book {}>'.format(self.borrowed_book)


    @classmethod
    def borrow_book(cls, borrowed_book, user_id):
        """Creates a borrowed book and ensures that the book is available for borrowing"""
        in_books = Book.query.filter_by(book=borrowed_book).first()

        if in_books is None:
            return make_response(jsonify({
                "message" : "kindly include the book in library before adding it to borrowed books"}), 400)

        if in_books.copies > 0:
            new_borrowed = cls(borrowed_book=borrowed_book, book_id=in_books.id, returned=False, user_id=user_id)
            db.session.add(new_borrowed)
            in_books.copies -= 1
            db.session.commit()

            user = User.query.filter_by(id=user_id).first()
            History.create_history(book=borrowed_book, borrowed_id=new_borrowed.id,
                                    book_id=in_books.id, borrower=user.username,
                                    user_id=user.id)
            
            return make_response(jsonify({
                "message" : "borrowed book has been successfully created",
                str(new_borrowed.id) : {"borrowed_book" : new_borrowed.borrowed_book,
                                    "author" : in_books.author}}), 201)

        return make_response(jsonify({
            "message" : "all the copies of that book have been borrowed"}), 400)

    @staticmethod
    def delete_book(borrowed_id):
        """Deletes a borrowed book from borrowed book list"""
        book = Borrowed.query.filter_by(id=borrowed_id).first()

        if book is None:
            return make_response(jsonify({"message" : "borrowed book does not exists"}), 404)

        db.session.delete(book)
        db.session.commit()
        return make_response(jsonify({
            "message" : "borrowed book has been successfully deleted"}), 200)
    
    @staticmethod
    def return_borrowed(borrowed_id):
        """Deletes a borrowed book from borrowed book list"""
        book = Borrowed.query.get(borrowed_id)
        
        if book is None:
            return make_response(jsonify({"message" : "borrowed book does not exists"}), 404)

        in_books = Book.query.filter_by(id=book.book.id).first()
        
        in_books.copies += 1
        book.returned = True
        History.update_returned(borrowed_id)
        db.session.commit()
        return make_response(jsonify({
            "message" : "borrowed book has been successfully returned"}), 200)

    @staticmethod
    def get_borrowed(borrowed_id):
        """Gets a particular borrowed_book"""
        borrow = Borrowed.query.filter_by(id=borrowed_id).first()

        if borrow is None:
            return make_response(jsonify({"message" : "borrowed book does not exists"}), 404)

        info = {borrow.id : {"book_id" : borrow.book.id, "book": borrow.book.book,
                "borrower" : borrow.user.username, "email" : borrow.user.email,
                "returned" : borrow.returned}}

        return make_response(jsonify({"borrowed_book" : info}), 200)


    @staticmethod
    def get_all_borrowed():
        """Gets all borrowed_books"""
        borrowed = Borrowed.query.all()

        if borrowed != None:
            borrowed_list = []
            for borrow in borrowed:
                info = {borrow.id : {"book_id" : borrow.book.id, "book": borrow.book.book,
                        "borrower" : borrow.user.username, "author" : borrow.book.author,
                        "returned" : borrow.returned}}
                borrowed_list.append(info)

            return make_response(jsonify({"borrowed_books" : borrowed_list}), 200)
        return make_response(jsonify({"message" : "borrowed book does not exists"}), 404)


class History(db.Model):
    """Contains book columns and methods to add, update and delete a book"""
    

    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(250), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    borrower = db.Column(db.String(250), nullable=False, unique=False)
    borrowed_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    datetimeborrowed = db.Column(db.DateTime, nullable=False)
    datetimereturned = db.Column(db.DateTime, nullable=True)
    returned = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        return '<history {}>'.format(self.history)
    
    @classmethod
    def create_history(cls, book, book_id, borrowed_id, borrower, user_id):
        """Creates a new history and ensures it is saved"""
        new_history = cls(book=book, book_id=book_id,
                            borrower=borrower, borrowed_id=borrowed_id,
                            user_id=user_id, datetimeborrowed=datetime.datetime.utcnow(),
                            returned=False)
        db.session.add(new_history)
        db.session.commit()    

    @staticmethod
    def get_all_history():
        """Gets all history"""
        all_history = []
        history = History.query.all()

        if history != None:
            for record in history:
                info = {record.id : {"book_id" : record.book_id, "book" : record.book, "user" : record.borrower,
                    "user id" : record.user_id, "datetime borrowed" : record.datetimeborrowed, "datetime returned" : record.datetimereturned,
                    "returned" : record.returned}}
                all_history.append(info)

            return make_response(jsonify({"All History" : all_history}), 200)
        return make_response(jsonify({"All History" : all_history}), 200)
        
    
    @staticmethod
    def get_all_bookhistory(book_id):
        """Gets all history"""
        in_books = Book.query.filter_by(id=book_id).first()
        history = History.query.filter_by(book_id=book_id).all()

        book_history = []
        if in_books != None and history != None:
            if history != None:
                for record in history:
                    info = {record.id : {"book_id" : record.book_id, "user" : record.borrower,
                        "user id" : record.user_id, "datetime borrowed" : record.datetimeborrowed, "datetime returned" : record.datetimereturned,
                        "returned" : record.returned}}
                    book_history.append(info)
                
                book = Book.query.filter_by(id=book_id).first()
                return make_response(jsonify({in_books.book : book_history}), 200)
            return make_response(jsonify({in_books.book : book_history}), 200)
        return make_response(jsonify({"message" : "The book does not exist"}), 404)
    
    @staticmethod
    def get_all_userhistory(user_id):
        """Gets all history"""
        in_users = User.query.filter_by(id=user_id).first()
        history = History.query.filter_by(user_id=user_id).all()
        user_history = []

        if in_users != None and history != None:
            if history is None:
                for record in history:
                    info = {record.id : {"book_id" : record.book_id, "book" : record.book,
                        "user id" : record.user_id,  "datetime borrowed" : record.datetimeborrowed, "datetime returned" : record.datetimereturned,
                        "returned" : record.returned}}
                    user_history.append(info)
                    return make_response(jsonify({in_users.username : user_history}), 200)
            return make_response(jsonify({in_users.username : user_history}), 200)
        return make_response(jsonify({"message" : "No record of that user exists"}), 404)

    @staticmethod
    def update_returned(borrowed_id):
        """returns book and adds timestamp to it"""
        history = History.query.filter_by(borrowed_id=borrowed_id).first()

        history.datetimereturned = datetime.datetime.utcnow()
        history.returned = True
        db.session.commit()

        return history
    