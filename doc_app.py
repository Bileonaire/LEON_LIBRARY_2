"""Contain interactive documentation to help one get started using the API
"""
import os

from flasgger import Swagger

from app import create_app


app = create_app('config.ProductionConfig')
swagger = Swagger(app)


# Users
@app.route('/api/v2/auth/register/', methods=["POST"])
def signup():
    """ endpoint for registering users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
    """

@app.route('/api/v2/auth/login', methods=["POST"])
def login():
    """ endpoint for logging in users.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: password
        required: true
    """

# will be secured in the near future
@app.route('/api/v2/users', methods=["POST"])
def users_create():
    """ endpoint for creating users.
    ---
    parameters:
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: admin
        in: formData
        type: boolean
        required: false
        default: false
    """

@app.route("/api/v2/users", methods=["GET"])
def get_all_users():
    """endpoint for  getting all users.
     ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v2/users/<int:user_id>", methods=["GET"])
def get_one_user():
    """endpoint for  getting a particular user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v2/users/<int:user_id>', methods=["PUT"])
def update_user():
    """ endpoint for updating an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: username
        required: true
        in: formData
        type: string
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
      - name: confirm_password
        in: formData
        type: string
        required: true
      - name: id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v2/users/<int:user_id>', methods=["DELETE"])
def delete_user():
    """ endpoint for deleting an existing user.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: user_id
        in: path
        type: integer
        required: true
    """


# Meals
@app.route('/api/v2/books', methods=["POST"])
def create_book():
    """ endpoint for creating a meal item.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: book
        required: true
        in: formData
        type: string
      - name: copies
        in: formData
        type: float
        required: true
      - name: author
        required: false
        in: formData
        type: string

    """

@app.route("/api/v2/books", methods=["GET"])
def get_all_books():
    """endpoint for getting all books.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v2/books/<int:book_id>", methods=["GET"])
def get_one_book():
    """endpoint for  getting a particular book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: book_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v2/books/<int:book_id>', methods=["PUT"])
def update_book():
    """ endpoint for updating an existing book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: book
        required: true
        in: formData
        type: string
      - name: copies
        in: formData
        type: float
        required: true
      - name: author
        required: false
        in: formData
        type: string
      - name: book_id
        required: true
        in: path
        type: integer
      
    """

@app.route('/api/v2/books/<int:book_id>', methods=["DELETE"])
def delete_book():
    """ endpoint for deleting an existing book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: book_id
        in: path
        type: integer
        required: true
    """


# Borrowed
@app.route('/api/v2/borrowed', methods=["POST"])
def create_borrowed():
    """ endpoint for creating a borrowed book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: borrowed_book
        required: true
        in: formData
        type: string
      - name: returned
        required: false
        in: formData
        type: boolean
    """

@app.route("/api/v2/borrowed", methods=["GET"])
def get_all_borrowed():
    """endpoint for  getting all borrowed books.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
    """

@app.route("/api/v2/borrowed/<int:borrowed_id>", methods=["GET"])
def get_one_borrowed_book():
    """endpoint for getting a particular borrowed book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: borrowed_id
        in: path
        type: integer
        required: true
    """

@app.route('/api/v2/borrowed/<int:borrowed_id>', methods=["PUT"])
def update_borrowed():
    """ endpoint for updating an existing borrowed book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: borrowed_book
        required: true
        in: formData
        type: string
      - name: returned
        required: false
        in: formData
        type: boolean
    """

@app.route('/api/v2/borrowed/<int:borrowed_id>', methods=["DELETE"])
def delete_borrowed():
    """ endpoint for deleting an existing borrowed book.
    ---
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
      - name: borrowed_id
        in: path
        type: integer
        required: true
    """

@app.route('/')
def hello_world():
    "test that flask app is running"
    return "To view the docs visit: https://leonlibrary.herokuapp.com/apidocs"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
