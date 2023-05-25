from flask import request, render_template
import requests
from app import app
from .forms import PokemonForm, LoginForm, SignUpForm

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/pokemon_search', methods=['GET', 'POST'])
def pokemon_search():
    form = PokemonForm()
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')
        
        def getPokemonInfo():
            base_url = 'https://pokeapi.co/'
            url = f'{base_url}api/v2/pokemon/{pokemon}'
            response = requests.get(url)
            if response.ok:
                data = response.json()
                front_shiny = data['sprites']['front_shiny']
                ability = data['abilities'][0]['ability']['name']
                base_experience = data['base_experience']
                hp_stat = data['stats'][0]['base_stat']
                attack_stat = data['stats'][1]['base_stat']
                defense_stat = data['stats'][2]['base_stat']
                
                return {
                    'name': pokemon,
                    'front_shiny': front_shiny,
                    'ability': ability,
                    'base_experience': base_experience,
                    'hp_stat': hp_stat,
                    'attack_stat': attack_stat,
                    'defense_stat': defense_stat
                }
            else:
                return "Pokemon not found"

        pokemon_info = getPokemonInfo()
        return render_template('pokemon_search.html', form=form, pokemon_info=pokemon_info)

    return render_template('pokemon_search.html', form=form)


REGISTERED_USERS = {
    'seanbor123@gmail.com': {
        'name': 'Sean',
        'password': 'ilovemydog'
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            return f"Hello, {REGISTERED_USERS[email]['name']}"
        else:
            return f'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        name = form.first_name.data + " " + form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        REGISTERED_USERS[email] = {
            'name': name,
            'password': password
        }
        return 'Thank you for signing up!'
    else:
        return render_template('signup.html', form=form)
