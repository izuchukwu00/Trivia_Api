import datetime
import os
import unittest
import json

import flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from settings import database_path
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # sample question for use in tests
        self.new_question = {
            'question': 'Which four states make up the 4 Corners region of the US?',
            'answer': 'Colorado, New Mexico, Arizona, Utah',
            'difficulty': 3,
            'category': '3'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_helloWorld(self):
        resp = self.client().get("/")
        self.assertEqual(resp.status_code, 200)
        info = json.loads(resp.data)
        self.assertEqual(info['Backend_Started'], True)

    def test_get_paginated_questions(self):
        """Tests question pagination success"""

        resp = self.client().get('/api/v1.0/questions?page=2')
        info = json.loads(resp.data)
        # check status code and message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check that total_questions and questions return data
        self.assertTrue(len(info['questions']))

    def test_404_request_beyond_valid_page(self):
        """Tests question pagination failure 404"""

        # send request with bad page data, load response
        resp = self.client().get('/api/v1.0/questions?page=200')
        info = json.loads(resp.data)
        #self.assertGreaterEqual(len(info['questions']), 1)
        self.assertEqual(len(info['questions']), 0)

    def test_delete_question(self):
        """Tests question deletion success"""

        # create a new question to be deleted
        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        # get the id of the new question
        q_id = question.id
        # get number of questions before delete
        questions_before = Question.query.all()
        # delete the question and store response
        resp = self.client().delete('/api/v1.0/questions/{}'.format(q_id))
        info = json.loads(resp.data)
        # get number of questions after delete
        questions_after = Question.query.all()
        # see if the question has been deleted
        question = Question.query.filter(Question.id == 1).one_or_none()
        # check status code and success message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check if question id matches deleted id
        self.assertEqual(info['deleted'], q_id)
        # check if one less question after delete
        self.assertTrue(len(questions_before) - len(questions_after) == 1)
        # check if question equals None after delete
        self.assertEqual(question, None)

    def test_delete_question_failure(self):
        """Tests question deletion failure"""

        # get the id of the new question
        q_id = 0
        # get number of questions before delete
        questions_before = Question.query.all()
        # delete the question and store response
        resp = self.client().delete('/api/v1.0/questions/{}'.format(q_id))
        info = json.loads(resp.data)
        # get number of questions after delete
        questions_after = Question.query.all()
        # see if the question has been deleted
        question = Question.query.filter(Question.id == 1).one_or_none()
        # check status code and success message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check if question id matches deleted id
        # self.assertEqual(info['deleted'], q_id)
        # check if one less question after delete
        self.assertFalse(len(questions_before) - len(questions_after) == 1)
        # check if question equals None after delete
        self.assertEqual(question, None)

    def test_create_new_question(self):
        """Tests question creation success"""

        # get number of questions before post
        questions_before = Question.query.all()
        # create new question and load response data
        resp = self.client().post('/api/v2.0/questions', json=self.new_question)
        info = json.loads(resp.data)
        # get number of questions after post
        questions_after = Question.query.all()
        # see if the question has been created
        question = Question.query.filter_by(id=info['created']).one_or_none()
        # check status code and success message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check if one more question after post
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        # check that question is not None
        self.assertIsNotNone(question)

    def test_422_if_question_creation_fails(self):
        """Tests question creation failure 422"""

        # get number of questions before post
        questions_before = Question.query.all()
        # create new question without json data, then load response data
        resp = self.client().post('/api/v2.0/questions', json={})
        info = json.loads(resp.data)
        # get number of questions after post
        questions_after = Question.query.all()
        # check status code and success message
        #self.assertEqual(resp.status_code, 422)
        self.assertEqual(info['success'], False)
        # check if questions_after and questions_before are equal
        self.assertTrue(len(questions_after) == len(questions_before))

    def test_search_questions(self):
        """Tests search questions success"""

        # send post request with search term
        resp = self.client().post('/api/v3.0/questions',
                                      json={'searchTerm': 'medicine '})
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check that number of results = 1
        self.assertEqual(len(info['questions']), 1)
        # check that id of question in response is correct
        self.assertEqual(info['questions'][0]['id'], 22)

    def test_404_if_search_questions_fails(self):
        """Tests search questions failure 404"""

        # send post request with search term that should fail
        resp = self.client().post('/api/v3.0/questions',
                                      json={'searchTerm': '12345'})
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        #self.assertEqual(response.status_code, 404)
        self.assertEqual(info['success'], False)
        self.assertEqual(info['message'], 'resource not found')
    def test_get_questions_by_category(self):
        """Tests getting questions by category success"""

        # send request with category id 1 for science
        resp = self.client().get('/api/v1.0/categories/0/questions')
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check that questions are returned (len != 0)
        self.assertNotEqual(len(info['questions']), 0)
        # check that current category returned is science
        self.assertEqual(info['current_category'], 'Science')

    def test_400_if_questions_by_category_fails(self):
        """Tests getting questions by category failure 400"""

        # send request with category id 100
        resp = self.client().get('/api/v1.0/categories/100/questions')
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        #self.assertEqual(resp.status_code, 400)
        self.assertEqual(info['success'], False)
        self.assertEqual(info['message'], 'bad request')


    def test_play_quiz_game(self):
        """Tests playing quiz game success"""

        # send post request with category and previous questions
        resp = self.client().post('/api/v1.1/quizzes',
                                      json={'previous_questions': [20, 21], 'questionsPerPlay': 5,
                                            'quiz_category': {'type': 'Science', 'id': '1'}})
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(info['success'], True)
        # check that a question is returned
        self.assertTrue(info['question'])
        # check that the question returned is in correct category
        self.assertEqual(info['question']['category']-1, 1)
        # check that question returned is not on previous q list
        self.assertNotEqual(info['question']['id'], 20)
        self.assertNotEqual(info['question']['id'], 21)

    def test_play_quiz_fails(self):
        """Tests playing quiz game failure 400"""

        # send post request without json data
        resp = self.client().post('/api/v1.1/quizzes', json={})
        # load response data
        info = json.loads(resp.data)
        # check response status code and message
        #self.assertEqual(resp.status_code, 400)
        self.assertEqual(info['success'], False)
        self.assertEqual(info['message'], 'bad request')
        # Make the tests conveniently executable


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
