# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```
### OR
```bash
psql -U postgres trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.1/categories'`
  * Returns all the categories
  * URI:- http://127.0.0.1:5000/api/v1.1/categories
  * Response
```json
{
      "categories": {
          "1": "history",
          "2": "science",
          "3" : "Geography",
          "4" : "History",
          "5" : "Entertainment",
          "6" : "Sports"
          },
      "success": true
          }
```


`POST '/api/v2.0/questions'`
  * URI:- http://127.0.0.1:5000/api/v2.0/questions

  * Sends a post request to add new questions to database
```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```
- Response: Alerts on success


`POST '/api/v3.0/questions'`
  * URI:- http://127.0.0.1:5000/api/v3.0/questions
  * 
  * Sends a post request in order to get the questions by a search term
```json
{
      "search_term": "search_term",
      "success": true
          }
```
  * Response
```json
{
  "questions": {
             "id": 0,
             "question": "question",
             "category": "Science",
             "answer": "answer",
             "difficulty": 1
             }, 
  "total_questions": 5,
  "current_category": "Science", 
  "success": true
}
```

`POST '/api/v1.1/quizzes'`
  * Sends a post request in order to get the next question, whose id is not in the previous questions
  * URI:- http://127.0.0.1:5000/api/v1.1/quizzes
    Request Body:
```json
{
    "previous_questions": [1, 4],
    "quiz_category": "Science"
 }
```
  * Response
```json
{
      "question": [1, 4, 20], 
      "total_que_answered": 4, 
      "questionsPerPlay": 4, 
      "quiz_category_id": "1",
      "success": true
                                         
          }
```
`GET '/api/v1.0/categories/${cat}/questions'`
* URI:- http://127.0.0.1:5000/api/v1.0/categories/0/questions

- Fetches a dictionary of questions in which the keys are the ids and the value is the corresponding 
    string of the questions based on a selected category; success value
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs. 
- ie returns the all the questions in a selected category
```json
{
  "questions": {
             "id": 0,
             "question": "question",
             "category": "Science",
             "answer": "answer",
             "difficulty": 1
             }, 
  "total_questions": 5,
  "current_category": "Science", 
  "success": true
}
```

`GET '/api/v1.0/questions'`
* URI:- http://127.0.0.1:5000/api/v1.0/questions?page=1

- Returns the all the questions in a selected page/ pagination

```json
{   "questions": {
             "question": "question",
             "category": "Science",
             "answer": "answer",
             "difficulty": 1
             }, 
     "categories": ["Science", "Art", "Geography", "History", "Entertainment", "Sports"], 
     "total_questions": 19,
     "QUESTIONS_PER_PAGE": 10, 
     "success": true}
```

`GET '/api/v2.0/categories'`
* URI:- http://127.0.0.1:5000/api/v2.0/categories

- Returns a list of all categories

```json
    {   
     "categories": ["Science", "Art", "Geography", "History", "Entertainment", "Sports"]
     }
```

`DELETE '/api/v1.0/questions/${id}'`
* URI:- http://127.0.0.1:5000/api/v1.0/questions/1

- Returns the id of the deleted question and success value

```json
{
  "deleted": 1,
  "success": true
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql -U postgres -p 5432 trivia_test < trivia.psql
python test_flaskr.py
```

### OR
```bash
#dropdb -U postgres -p 5432 trivia_test
createdb -U postgres -p 5432 trivia_test
psql -U postgres -p 5432 trivia_test < trivia.psql
python test_flaskr.py
```
