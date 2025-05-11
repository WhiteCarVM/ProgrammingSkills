from flask import Flask, request, render_template_string, make_response
import time

"""
1. Run: python app.py
2. GET Method Testing:
    1) http://localhost:5000/?method=GET
    2) http://localhost:5000/login?username=admin&password=123
3. POST Method Testing:
    1) http://localhost:5000/?method=POST
    2) Send requests
"""

app = Flask(__name__)

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Test</title>
</head>
<body>
    <h2>Login Form</h2>
    <form method="{{ method }}" action="/login">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <p>Try to brute-force this form!</p>
    {% if message %}
        <p style="color: red;">{{ message }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    method = request.args.get('method', 'POST')
    return render_template_string(HTML, method=method)

@app.route('/login', methods=['GET', 'POST'])
def login():
    time.sleep(0.5)
    
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return "Success! Valid credentials: {}:{}".format(username, password)
    else:
        return "Invalid credentials", 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)