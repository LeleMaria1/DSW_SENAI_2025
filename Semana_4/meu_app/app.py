# Importa as classes e funções necessárias
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# 1. CONFIGURAÇÃO DA APLICAÇÃO
app = Flask(__name__)

# A SECRET_KEY é crucial para a proteção CSRF. 
# Em um projeto real, isso deve ser uma string complexa e mantida em segredo.
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-dificil-de-adivinhar'

# 2. DEFINIÇÃO DA CLASSE DO FORMULÁRIO EXISTENTE
class MeuFormulario(FlaskForm):
    """
    Representa o formulário de contato com validação.
    """
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    email = StringField('Seu Melhor E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."), 
        Email(message="Por favor, insira um e-mail válido.")
    ])
    submit = SubmitField('Enviar Cadastro')

# 3. DEFINIÇÃO DA CLASSE DO NOVO FORMULÁRIO DE REGISTRO
class FormularioRegistro(FlaskForm):
    """
    Formulário de registro de usuário com campos avançados.
    """
    nome = StringField('Nome Completo', validators=[DataRequired(message="Este campo é obrigatório.")])
    email = StringField('E-mail', validators=[
        DataRequired(message="Este campo é obrigatório."),
        Email(message="E-mail inválido.")
    ])
    # PasswordField esconde o texto digitado
    senha = PasswordField('Senha', validators=[
        DataRequired(message="A senha é obrigatória."),
        Length(min=8, message="A senha deve ter no mínimo 8 caracteres.")
    ])
    # EqualTo valida que o campo de confirmação é igual ao campo 'senha'
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message="Confirme sua senha."),
        EqualTo('senha', message="As senhas devem ser idênticas.")
    ])
    # TextAreaField é para campos de texto longos
    biografia = TextAreaField('Biografia (opcional)')
    # BooleanField é para caixas de seleção (checkboxes)
    aceitar_termos = BooleanField('Aceito os Termos de Serviço', validators=[
        DataRequired(message="Você deve aceitar os termos.")
    ])
    submit = SubmitField('Registrar')

# 4. CRIAÇÃO DAS ROTAS (VIEWS)

# Rota original, com o formulário em branco
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = MeuFormulario()
    if form.validate_on_submit():
        nome_usuario = form.nome.data
        email_usuario = form.email.data
        flash(f'Cadastro recebido com sucesso para {nome_usuario} ({email_usuario})!', 'success')
        return redirect(url_for('formulario'))
        
    return render_template('formulario.html', form=form)

# --- EXEMPLOS DE PREENCHIMENTO ---
@app.route('/formulario/preenchido-args', methods=['GET', 'POST'])
def formulario_com_argumentos():
    form = MeuFormulario(nome="Fulano de Tal", email="fulano@exemplo.com")
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_argumentos'))
    return render_template('formulario.html', form=form)

@app.route('/formulario/preenchido-obj', methods=['GET', 'POST'])
def formulario_com_objeto():
    class UsuarioMock:
        def __init__(self, nome, email):
            self.nome = nome
            self.email = email
            
    usuario_do_banco = UsuarioMock(nome="Ciclano da Silva", email="ciclano@banco.com")
    form = MeuFormulario(obj=usuario_do_banco)
    if form.validate_on_submit():
        flash(f'Dados de "{form.nome.data}" atualizados com sucesso!', 'success')
        return redirect(url_for('formulario_com_objeto'))
    return render_template('formulario.html', form=form)

# 5. NOVA ROTA PARA O FORMULÁRIO DE REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Renderiza e processa o formulário de registro avançado.
    """
    form = FormularioRegistro()
    
    if form.validate_on_submit():
        # Captura os dados para a mensagem de flash
        nome = form.nome.data
        biografia = form.biografia.data
        
        # Desafio Extra: Inclui a biografia na mensagem flash se ela foi preenchida
        flash_message = f'Olá, {nome}! Seu registro foi concluído com sucesso.'
        if biografia:
            flash_message += f' Sobre você: "{biografia}".'
        
        flash(flash_message, 'success')
        return redirect(url_for('registro'))
        
    return render_template('registro.html', form=form)

# Rota principal agora renderiza um template HTML
@app.route('/')
def index():
    """
    Renderiza a página inicial a partir de um arquivo de template.
    """
    return render_template('index.html')

# Permite executar o app diretamente com 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)