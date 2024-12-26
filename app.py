import os
from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS


# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Créer le dossier 'instance' si nécessaire
instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Configuration de la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "dbprovisoire.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'x8rULdOHjujoXUhffchOJ2iZ1I0KJxQu'

# Initialisation des extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modèle utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="membre")
    is_verified = db.Column(db.Integer, default=0)

# Créer la base de données
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Rediriger l'utilisateur vers la route /register
    return redirect(url_for('register'))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    password = data.get('password')

    # Vérification des champs
    if not all([nom, prenom, email, password]):
        return jsonify({"message": "Tous les champs sont obligatoires"}), 400

    # Vérifier si l'email existe déjà
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Cet email est déjà enregistré"}), 400

    # Hasher le mot de passe
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Créer un nouvel utilisateur
    new_user = User(nom=nom, prenom=prenom, email=email, password=hashed_password)

    # Ajouter à la base de données
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Utilisateur enregistré avec succès"}), 201

if __name__ == '__main__':
    app.run(debug=True)
