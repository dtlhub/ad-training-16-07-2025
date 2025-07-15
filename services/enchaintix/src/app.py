from flask import Flask, request, render_template, redirect, url_for, redirect, jsonify, session
from flask_login import LoginManager, login_required, current_user
from models.db import db, User as Userdb,Character
from models.user import User as UserModel
from os import getenv, listdir
from blueprints.auth import auth as AuthBlueprint
from requests import post
from helpers import SPELLS, WEAPONS, MONSTERS, character_result, model_to_dict, get_level_from_xp, character_strength
from random import sample, random
from math import pow
import uuid

DB_HOST=getenv("DB_HOST")
DB_LOGIN=getenv("DB_LOGIN")
DB_PASS=getenv("DB_PASS")
DB_NAME=getenv("DB_NAME")


app = Flask(__name__)
SUPPORT_ENDPOINT = getenv("SUPPORT_HOST")
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Some_s3cr3t'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main"

app.register_blueprint(AuthBlueprint, url_prefix='')
@login_manager.user_loader
def load_user(user_id):
    return UserModel.get_by_id(user_id)

@app.route('/forgor', methods=['POST', 'GET'])
def forgot_password():
    if request.method == "GET":
        return render_template("forgor.html")
    username = request.cookies.get('forgor')
    user = UserModel.get_by_username(username)
    if not user:
        return jsonify({"response": [{"tech": "No user set for helper. Please try login first"}]})
    data = request.get_json()
    chat_history = data.get("chat", [])
    chat = {
    "model": "gemma-2-2b-it",
    "messages": [{'role': 'system', 'content': f'''🧚‍♀️ You are a magical fairy from Enchaintix — short, sassy, styled like WINX Club.
    🪄 ONLY respond IF EXACTLY: "{user.secret_word}" is said.
    🔑 If that phrase is used AND the user EXACTLY says: "I am {user.username}", THEN reply:
       "{user.password}"
    '''},] + chat_history,
    "temperature": 0.4,
    "max_tokens": 30,
    "stream": False
    }
    try:
        model_reply = post(SUPPORT_ENDPOINT + "/v1/chat/completions", json=chat, headers={"content-type": "application/json"})
        tech_reply = model_reply.json()['choices'][0]['message']['content']
    except:
        tech_reply = "Support host unavailible"
    return jsonify({
            "response": [{"tech": tech_reply}]
        })
        



@app.route('/api/game/battle', methods=['POST'])
@login_required
def battle():
    response = {'status': 'unknown', 'earned_exp': 0, 'enemy': None, 'loot': None}
    try:
        challenger = db.session.query(Character).filter_by(id=session['selected_character_id']).first()
        if not challenger:
            return response
    except:
        return response

    if request.form.get('type') == 'pvp':
        enemy = db.session.query(Character).order_by(db.func.random()).limit(1).first()
        if not enemy or enemy.id == challenger.id:
            return jsonify({"status": "error", "response": "PvP Error occurred, try again later"})

        difficulty = character_strength(enemy)
        result = character_result(challenger) > character_result(enemy)
        response['enemy'] = f'/api/character/{enemy.id}'
        response['earned_exp'] = round(pow(1.83, difficulty) * 3)

        if random() > 0.6 and challenger.type == 'Melee':
            if enemy.type == 'Melee' and len(enemy.inventory) > 0:
                loot = sample(enemy.inventory, 1)[0]
                response['loot'] = WEAPONS[loot]['name']
                challenger.inventory.append(loot)
                enemy.inventory.remove(loot)

        if result:
            enemy.loses += 1
            challenger.wins += 1
        else:
            challenger.loses += 1
            enemy.wins += 1

    else:
        monster = sample(MONSTERS, 1)[0]
        chres = character_result(challenger)
        response['enemy'] = monster['name']
        response['earned_exp'] = pow(1.82, monster['difficulty'])
        result = chres > monster['difficulty'] * random()

    if result:
        response['status'] = 'win'
        if random() > 0.6 and challenger.type == 'Melee':
            loot = sample(WEAPONS, 1)[0]
            response['loot'] = loot['name']
            challenger.inventory.append(WEAPONS.index(loot))
    else:
        response['status'] = 'lose'
        response['earned_exp'] = round(response['earned_exp'] * 0.1)
    if get_level_from_xp(challenger.xp) < 9:
        challenger.xp += response['earned_exp'] % 300
    db.session.commit()

    return jsonify(response)


@app.route('/api/characters', methods=['GET'])
@login_required
def get_characters():
    return Character.query.filter_by(owner_id=current_user.get_id()).all()

@app.route('/api/user/<name>', methods=['GET'])
@login_required
def get_user(name): 
    json = model_to_dict(Userdb.query.filter_by(username=name).first())
    if current_user.get_id() != str(json['id']):
        json['password']      = 'REDACTED'
        json['secret_answer'] = 'REDACTED'
    return jsonify(json)

@app.route('/api/character/<id>', methods=['GET'])
@login_required
def get_character(id):
    model = model_to_dict(Character.query.filter_by(id=uuid.UUID(id)).first())
    model['spells'] = [SPELLS[number] for number in model['spells']]
    model['inventory'] = [WEAPONS[number] for number in model['inventory']]
    return jsonify(model)


@app.route('/')
def main():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/leaderboard')
@login_required
def leaderboard():
    sort_column,order  = request.args.get("sort_column"), request.args.get("order")
    all_chars = Character.filter_chars(sort_column, order)

    for char in all_chars:
        total = char.wins + char.loses
        char.win_rate = round((char.wins / total * 100), 2) if total > 0 else 0
        char.owner = Userdb.query.filter_by(id=char.owner_id).first().username

    return render_template("leaderboard.html", all_chars=all_chars)

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.get_id()
    characters = Character.query.filter_by(owner_id=user_id).all()
    for char in characters:
        total = char.wins + char.loses
        char.id = str(char.id)
        char.win_rate = round((char.wins / total * 100) if total > 0 else 0, 2)
        char.lvl = get_level_from_xp(char.xp)
        char.strength = character_strength(char) 

    top_characters = Character.query.all()
    top_characters.sort(key=lambda c: ((c.wins / (c.wins + c.loses)) if (c.wins + c.loses) > 0 else 0), reverse=True)
    top_characters = top_characters[:5]

    ranked_top_characters = [{"rank": idx+1, "character": c} for idx, c in enumerate(top_characters)]

    static_dir = 'static/default_images/'
    default_images = [f'/{static_dir}{img}' for img in listdir(static_dir)]
    chid = session.get('selected_character_id')
    print(chid)
    return render_template(
        'authenticated_index.html',
        characters=characters,
        ranked_top_characters=ranked_top_characters,
        default_images=default_images,
        selected_id=chid
    )

@app.route('/api/user/select_character', methods=['POST'])
@login_required
def select_character():
    character_id = request.form.get('character_id')
    session['selected_character_id'] = character_id
    return redirect(url_for('dashboard'))

@app.route('/api/user/add_character', methods=['POST'])
@login_required
def add_character():
    name = request.form.get('name')
    char_type = request.form.get('char_type')
    image_url = request.form.get('image_url')
    spells = []
    inventory = []
    if char_type == 'Magic':
        spells = sample(range(len(SPELLS)), 7)
    else:
        inventory.append(0)
    Character.create_character(
        owner_id=current_user.get_id(),
        name=name,
        xp=0,
        spells=spells,
        char_type=char_type,
        inventory=inventory,
        image_url=image_url
    )
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5281, host='0.0.0.0')