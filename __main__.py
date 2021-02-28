from flask import Flask
from pages.accueil import supprimer, accueil

app = Flask(__name__, template_folder='templates')

app.run(debug="on")