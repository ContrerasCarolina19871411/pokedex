from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
# creamos la cadena de conexion
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///pokedex.sqlite"

#vinculamos la base de datos 
db = SQLAlchemy(app)
#crear objeto
class Pokemon(db.Model):
    id: Mapped[int] = mapped_column(db.Integer,primary_key=True,autoincrement=True)
    name: Mapped[str]= mapped_column(db.String, nullable=False)
    height:Mapped[float]= mapped_column(db.Float,nullable=False)
    weight:Mapped[float]= mapped_column(db.Float,nullable=False)
    order:Mapped[int]= mapped_column(db.Integer,nullable=False)
    type:Mapped[str]= mapped_column(db.String,nullable=False)

with app.app_context():
    db.create_all()

def get_pokemon_data(pokemon):
    url= f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    r = requests.get(url).json()
    return r
#pruebas de base de datos
@app.route("/insert_pokemon/<pokemon>")
def insert(pokemon):
        new_pokemon= pokemon
        if new_pokemon:
             int(1.1)
             obj = Pokemon(pokemon)
             db.session.add(obj)
             db.session.commit()
        return 'Pokemon Agregado'

@app.route("/select")
def select():
    Lista_pokemon = Pokemon.query.all()
    for p in  Lista_pokemon:
     print (p.name)
    return 'alo'

@app.route("/select/<name>")
def selectbyname(name):
    poke = Pokemon.query.filter_by(name=name).first()
    return str(poke.id)

@app.route("/selectbyid/<id>")
def selectbyid(id):
    poke = Pokemon.query.filter_by(id=id).first()
    return str(poke.id) + str(poke.name)

@app.route("/deletebyid/<id>")
def deletebyid(id):
    pokemon_a_eliminar = Pokemon.query.filter_by(id=id).first()
    db.session.delete(pokemon_a_eliminar)
    db.session.commit()
    return 'Pokemon Eliminado'

@app.route("/",methods=['GET','POST'])
def home():
    pokemon = None
    if request.method == 'POST':
        name_pokemon = request.form.get('name')
        if name_pokemon:
            data = get_pokemon_data(name_pokemon.lower())
            pokemon={'id':1,
             'name':data.get('name').upper(),
             'height':data.get('height'),
             'weight':data.get('weight'),
             'order':data.get('order'),
             'type':'oscuro',
             'photo' :data.get('sprites').get('other').get('official-artwork').get('front_default')
                    }
    return render_template('pokemon.html',pokemon=pokemon)
   
@app.route("/detalle")
def detalle():
    return render_template("detalle.html")

if __name__=='__main__':
    app.run(debug=True)
