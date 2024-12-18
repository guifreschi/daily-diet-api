from flask import Flask, request, jsonify 
from models.user import User
from models.meals import Meals
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet-api-db"  

login_manager = LoginManager()
db.init_app(app) 
login_manager.init_app(app) 
login_manager.login_view = 'login' 

@login_manager.user_loader 
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
      login_user(user)
      return jsonify({"message": "Autenticação realizada com sucesso!"})

  return jsonify({"message": "Credenciais inválidas."}), 400

@app.route('/logout', methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/sign-up', methods=["POST"])
def sign_up():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password: 
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    user = User(username=username, password=hashed_password, role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"})

  return jsonify({"message": f"Dados inválidos: {'username' if not username else 'password'}"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
  user = User.query.get(id_user)
  if user:
    return {"username": user.username}

  return jsonify({"message": "Usuário não encontrado."}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
  data = request.json
  user = User.query.get(id_user)

  if id_user != current_user.id and current_user.role == 'user': 
    return jsonify({"message": "Operação não permitida."}), 403 

  if user and data.get("password"):
    user.password = data.get("password") 
    db.session.commit()
    return jsonify({"message": f"Usuário {user.id} atualizado com sucesso."})
  
  return jsonify({"message": "Usuário não encontrado."}), 404

@app.route("/user/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
  user = User.query.get(id_user)

  if current_user.role == 'user':
    return jsonify({"message": "Operação não permitida."}), 403 

  if id_user == current_user.id:
    return jsonify({"message": "Deleção não permitida."}), 403

  if user:
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} deletado com sucesso."})
  
  return jsonify({"message": "Usuário não encontrado."}), 404

@app.route("/user/meals", methods=["POST"])
@login_required
def add_meal():
  data = request.json
  user_id = current_user.id
  name = data.get("name")
  description = data.get("description")
  date_time = data.get("date_time")
  on_diet = data.get("on_diet")

  if name:
    meal = Meals(name=name, description=description, date_time=date_time, on_diet=on_diet, user_id=user_id)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição adicionada com sucesso!"})

  return jsonify({"message": "Dados inválidos"}), 400

@app.route("/user/meals", methods=["GET"])
@login_required
def read_meals():
  meals = Meals.query.filter_by(user_id=current_user.id)

  if meals:
    meals_data = [
              {"id": meal.id, "name": meal.name, "description": meal.description, "date": meal.date_time, "on_diet": meal.on_diet}
              for meal in meals
          ]
          
    return jsonify({"meals": meals_data}), 200
  
  return jsonify({"message": "Nenhuma refeição encontrada."}), 404

@app.route("/user/meal/<int:id_meal>", methods=["GET"])
@login_required
def read_meal(id_meal):
  meal = Meals.query.filter_by(user_id=current_user.id, id=id_meal).first()

  if meal:
    meal_data = {
        "id": meal.id,
        "name": meal.name,
        "description": meal.description,
        "date": meal.date_time,
        "on_diet": meal.on_diet
      }

    return jsonify({"meal": meal_data})
  
  return jsonify({"message": "Refeição não encontrada."}), 404

@app.route("/user/meal/<int:id_meal>", methods=["PUT"])
@login_required
def update_meal(id_meal):
  data = request.json
  meal = Meals.query.filter_by(user_id=current_user.id, id=id_meal).first()
  name = data.get("name")
  description = data.get("description")
  date = data.get("date_time")
  on_diet = data.get("on_diet")

  if meal and (name or description or date or on_diet is not None):
    if name is None:
      name = meal.name
    if description is None:
      description = meal.description
    if date is None:
      date = meal.date_time
    if on_diet is None:
      on_diet = meal.on_diet
    
    meal.name = name
    meal.description = description
    meal.date_time = date
    meal.on_diet = on_diet

    db.session.commit()
    return jsonify({"message": f"A refeição {meal.id} foi atualizada com sucesso."})

  return jsonify({"message": "Refeição não encontrada."}), 404

@app.route("/user/meal/<int:id_meal>", methods=["DELETE"])
@login_required
def delete_meal(id_meal):
  meal = Meals.query.filter_by(user_id=current_user.id, id=id_meal).first()

  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": f"Refeição {id_meal} deletada com sucesso."})
  
  return jsonify({"message": "Refeição não encontrada."}), 404

if __name__ == "__main__":
  app.run(debug=True)
