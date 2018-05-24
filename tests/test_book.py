"""Test the book endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class bookTests(BaseTests):
    """Tests functionality of the book endpoint"""


    def test_admin_get_one(self):
        """Tests admin successfully getting a book"""
        data = json.dumps({"book" : "book of legends", "author" : "bileonaire", "copies" : 45})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v2/books/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_user_get_one(self):
        """Tests user successfully getting a book"""
        data = json.dumps({"book" : "book of legends", "author" : "bileonaire", "copies" : 12})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v2/books/2', headers=self.user_header)
        self.assertEqual(response.status_code, 200)

    def test_get_non_existing(self):
        """Test getting a book while providing non-existing id"""
        response = self.app.get('/api/v2/books/10', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_book_update(self):
        """Test a successful book update"""
        initial_data = json.dumps({"book" : "book of legends", "author" : "bileonaire" , "copies" : 15})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        data = json.dumps({"book" : "book of l", "author" : "bon", "copies" : 90})
        response = self.app.put(
            '/api/v2/books/2', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_update_non_existing(self):
        """Test updating non_existing book"""
        data = json.dumps({"book" : "kkkkkkkk", "author" : "kkkk", "copies" : 4})
        response = self.app.put(
            '/api/v2/books/50', data=data,
            content_type='application/json',
            headers=self.admin_header)
        self.assertEqual(response.status_code, 404)

    def test_good_deletion(self):
        """Test a successful book deletion"""
        initial_data = json.dumps({"book" : "kennniiiii", "author" : "bileonaire", "copies" : 3})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=initial_data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.delete('/api/v2/books/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_deleting_non_existing(self):
        """Test deleting book that does not exist"""
        response = self.app.delete('/api/v2/books/15', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_books(self):
        """Test getting all books"""
        response = self.app.get('/api/v2/books', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_returning_book_successful(self):
        """Tests user successfully returning a book"""
        data = json.dumps({"book" : "legends", "author" : "bileonaire", "copies" : 12})
        borrowed = json.dumps({"borrowed_book" : "legends"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        borrow_book = self.app.post( # pylint: disable=W0612
            '/api/v2/borrowed', data=borrowed,
            content_type='application/json',
            headers=self.user_header)
        response = self.app.put('/api/v2/borrowed/2', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_returning_book_unsuccessful(self):
        """Tests user unsuccessfully returning a book"""
        response = self.app.put('/api/v2/borrowed/76', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
