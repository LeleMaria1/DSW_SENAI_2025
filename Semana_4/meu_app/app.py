# Importa as classes e funções necessárias das bibliotecas
from flask import Flask, render_template, flash, redirect, url_for

#Importa a classe FlaskForm e os campos necessários do WTForms
from flask_wtf import FlaskForm

# Importa os campos e validadores necessários do WTForms
from wtforms import StringField, SubmitField

# Importa o validador DataRequired para garantir que os campos sejam preenchidos
from wtforms.validators import DataRequired

# Configura a chave secreta para o Flask-WTF
app = Flask(__name__)


app.config['SECRET_KEY'] = 'uma_chave_de_seguranca_muito_dificil'

class MeuFormulario(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(message='Campo obrigatório')])
    email = StringField('Email', validators=[DataRequired(message='Campo obrigatório'), Email(mesage='Por favor insira um email válido')])
    
    submit = SubmitField('Enviar')

#Definindo as rotas
@app.route('/')
def index():
    return render_template('index.html')

