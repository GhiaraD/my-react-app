from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change this in production
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Mock user database
users = {
    "admin@example.com": {
        "password": bcrypt.generate_password_hash("admin123").decode('utf-8'),
        "role": "admin"
    }
}

# Register endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users[email] = {"password": hashed_password, "role": "viewer"}  # Default role: viewer

    return jsonify({"message": "User registered successfully"}), 201

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users.get(email)
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"email": email, "role": user["role"]})
    return jsonify({"token": access_token})

# Protected route (Dashboard)
@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    return jsonify({"message": "Welcome to the protected dashboard!"})

if __name__ == '__main__':
    app.run(debug=True)
