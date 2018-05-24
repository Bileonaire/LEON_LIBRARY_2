"""Test the history endpoints on all methods and covers most edge cases
"""
import unittest
import json

import sys # fix import errors
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class HistoryTests(BaseTests):
    """Tests functionality of the history endpoint"""
    
    def test_admin_get_all_history(self):
        """Tests user successfully getting a book"""
        data = json.dumps({"book" : "legends", "author" : "bileonaire", "copies" : 12})
        borrowed = json.dumps({"borrowed_book" : "legends"})
        added_book = self.app.post( # pylint: disable=W0612
            '/api/v2/books', data=data,
            content_type='application/json',
            headers=self.admin_header)
        response = self.app.get('/api/v2/history', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)

    def test_admin_get_all_bookhistory(self):
        """Tests user successfully getting a book"""
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
        response = self.app.get('/api/v2/bookhistory/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_get_all_userhistory(self):
        """Tests user successfully getting a book"""
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
        response = self.app.get('/api/v2/bookhistory/1', headers=self.admin_header)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_failget_all_bookhistory(self):
        """Tests user unsuccessfully getting book history"""
        response = self.app.get('/api/v2/bookhistory/50', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)
    
    def test_admin_failget_all_userhistory(self):
        """Tests user unsuccessfully getting user history"""
        response = self.app.get('/api/v2/userhistory/50', headers=self.admin_header)
        self.assertEqual(response.status_code, 404)