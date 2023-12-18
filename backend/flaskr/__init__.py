import datetime
import os

import flask
from flask import Flask, request, abort, jsonify, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from flask_cors import CORS
import random
import os
from models import setup_db, Question, Category
from settings import database_path

SECRET_KEY = os.urandom(32)

# connect to a local trivia database
SQLALCHEMY_DATABASE_URI = database_path
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

QUESTIONS_PER_PAGE = 10

"""
@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
"""


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    setup_db(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.route("/")
    def helloWorld():
        data = flask.jsonify({"Backend_Started": True})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return data

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/api/v2.0/categories", methods=['GET'])
    def submit_cat():
        cat = session.query(Category)
        cate = [c.type for c in cat]
        response = flask.jsonify({'categories': cate,
                                  "QUESTIONS_PER_PAGE": QUESTIONS_PER_PAGE})
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/api/v1.0/questions", methods=['GET', 'POST'])
    def list_que():
        all_que = session.query(Question)
        cnt_que = len(list(all_que))

        page = int(request.args.get('page'))
        p = (page - 1) * QUESTIONS_PER_PAGE

        que = session.query(Question).offset(p).limit(QUESTIONS_PER_PAGE)
        cat = session.query(Category)

        ques = [
            {"id": q.id,
             "question": q.question,
             "category": q.category,
             "answer": q.answer,
             "difficulty": q.difficulty
             } for q in que]
        cate = [c.type for c in cat]

        # response = flask.jsonify({"questions": [{"id": 1, "question": 'Ford', "category": 1, "answer": 'true',
        # "difficulty": 2}], 'categories': "categories" ... })
        data = flask.jsonify({"questions": ques, 'categories': cate, "total_questions": cnt_que,
                              "QUESTIONS_PER_PAGE": QUESTIONS_PER_PAGE, "success": True})
        return data
        # return "user example"

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/api/v1.0/questions/<int:id>", methods=['DELETE'])
    def delete_que(id):
        try:
            session.query(Question).filter(Question.id == id).delete()
            session.commit()
            data = flask.jsonify({"success": True, "deleted": id})
            return data
        except:
            session.rollback()
            data = flask.jsonify({"success": False})
            return data

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/api/v2.0/questions", methods=['POST'])
    def submit_que():
        if request.method == 'POST':
            sc = flask.request.json
            try:
                que = Question(**sc)
                session.add(que)
                session.commit()
                #data = flask.jsonify({"success": True, "created": que.id})
                #return data

            except:
                session.rollback()
                data = flask.jsonify({"success": False})
                return data

            else:
                cat = session.query(Category)
                cate = [c.type for c in cat]
                data = flask.jsonify({'categories': cate, "success": True, "created": que.id})
                return data

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/api/v3.0/questions", methods=['POST'])
    def search_by_que():
        if request.method == 'POST':
            search_term = flask.request.json["searchTerm"]
            que = session.query(Question).filter(Question.question.ilike('%' + search_term + '%'))
            cnt_que = len(list(que))
            if cnt_que >= 1:
                ques = [
                    {"id": q.id,
                     "question": q.question,
                     "category": q.category,
                     "answer": q.answer,
                     "difficulty": q.difficulty
                     } for q in que]

                data = flask.jsonify({"questions": ques, "total_questions": cnt_que,
                                          "current_category": "", "success": True})
                return data
            else:
                data = flask.jsonify({"success": False, "message": "resource not found"})
                return data

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/api/v1.0/categories/<int:cat>/questions", methods=['GET'])
    def search_by_cate(cat):
        que = session.query(Question).filter(Question.category == str(cat + 1))
        #cate = session.query(Category).filter_by(id=cat+1).first().type
        #cate = session.query(Category).filter(Category.id == cat).first().type

        c = session.query(Category).filter_by(id=cat+1).one_or_none()
        if c is not None:
            category = c.type
        else:
            data = flask.jsonify({"success": False, "message": "bad request"})
            return data

        cnt_que = len(list(que))

        ques = [
            {"id": q.id,
             "question": q.question,
             "category": q.category,
             "answer": q.answer,
             "difficulty": q.difficulty
             } for q in que]

        data = flask.jsonify({"questions": ques, "total_questions": cnt_que,
                                  "current_category": category, "success": True})
        return data

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/api/v1.1/categories", methods=['GET'])
    def quiz():
        cat = session.query(Category)
        cate = [c.type for c in cat]
        data = flask.jsonify({"categories": cate, "success": True})
        return data

    @app.route("/api/v1.1/quizzes", methods=['POST'])
    def quizzes():
        try:
            p = flask.request.json

            p_que = p["previous_questions"]
            q_p_p = p["questionsPerPlay"]
            p_c_id = p["quiz_category"]["id"]

            if p_c_id == "all":
                que = session.query(Question)
            else:
                p_c = int(p_c_id) + 1
                que = session.query(Question).filter(Question.category == str(p_c))
                #for q in que:
                    #print(q.id)
            #print(p)

            ques = [
                {"id": q.id,
                 "question": q.question,
                 "category": q.category,
                 "answer": q.answer,
                 "difficulty": q.difficulty
                 } for q in que]
            try:
                dr = random.choice(list(filter(lambda d: d['id'] not in p_que, ques)))
                data = flask.jsonify({"question": dr, "total_que_answered": q_p_p, "questionsPerPlay": q_p_p, "success": True
                                          })
                return data
            except:
                data = flask.jsonify({"total_que_answered": len(ques), "success": True})
                return data
        except:
            return flask.jsonify({"success": False, "message": "bad request"})

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return 400

    @app.errorhandler(404)
    def not_found_error(error):
        return "404"

    @app.errorhandler(405)
    def MethodNotAllowed(error):
        return "405"
        #return jsonify(message="Method Not Allowed"), 405

    @app.errorhandler(422)
    def semantic_error(error):
        return "422"

    #@app.errorhandler(500)
    #def server_error(error):
        #return "500"

    return app
