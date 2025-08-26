# app.py - Projeto Receitinhas
# Importa as classes e funções necessárias do Flask.
from flask import Flask, render_template, request, redirect, url_for, flash

# Cria uma instância da aplicação.
app = Flask(__name__)

# Configura uma chave secreta para usar com flash messages.
app.config['SECRET_KEY'] = 'uma-chave-secreta-facil-para-receitinhas'

# ---- Rotas (URLs) da Aplicação ----
# Rota para a página inicial
@app.route('/')
def index():
    """Renderiza a página inicial com link para criar uma nova receita."""
    return render_template('index.html')

# Rota para o formulário de nova receita
@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    """
    Exibe um formulário para criar uma nova receita e processa o envio dos dados.
    Demonstra validação de formulários e redirecionamento com parâmetros.
    """
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome_receita = request.form['nome_receita']
        ingredientes = request.form['ingredientes']
        modo_preparo = request.form['modo_preparo']
        
        # Validação de campos obrigatórios
        if not nome_receita or not ingredientes or not modo_preparo:
            flash('Por favor, preencha todos os campos!', 'danger')
            return render_template('receita.html')
        
        # Redireciona para a página de receita criada, passando os dados
        return redirect(url_for('receita_criada', 
                              nome_receita=nome_receita, 
                              ingredientes=ingredientes, 
                              modo_preparo=modo_preparo))
    
    # Se a requisição for GET, exibe o formulário
    return render_template('receita.html')

# Rota para exibir a receita criada
@app.route('/receita-criada')
def receita_criada():
    """
    Exibe a receita criada com os dados enviados pelo formulário.
    """
    nome_receita = request.args.get('nome_receita', '')
    ingredientes = request.args.get('ingredientes', '')
    modo_preparo = request.args.get('modo_preparo', '')
    
    return render_template('receita_criada.html', 
                         nome_receita=nome_receita, 
                         ingredientes=ingredientes, 
                         modo_preparo=modo_preparo)

# ---- Executa a aplicação ----
if __name__ == '__main__':
    # Roda a aplicação no modo de depuração.
    app.run(debug=True)