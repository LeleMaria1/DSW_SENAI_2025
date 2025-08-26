# app.py - Projeto Receitinhas
# Importando as coisas que o Flask precisa pra funcionar
from flask import Flask, render_template, request, redirect, url_for, flash

# Criando o app Flask, que é o coração do nosso projeto
app = Flask(__name__)

# Definindo uma chave secreta pra usar mensagens flash (importante pra mostrar erros ou sucessos)
app.config['SECRET_KEY'] = 'uma-chave-secreta-facil-para-receitinhas'

# Criando uma lista vazia pra guardar as receitas (é como um caderno de receitas, mas na memória)
receitas = []

# ---- Rotas (URLs) da Aplicação ----
# Essa é a rota da página inicial, tipo a "capa" do site
@app.route('/')
def index():
    """Renderiza a página inicial com a lista de receitas cadastradas."""
    # Passa a lista de receitas pro template index.html pra mostrar na tela
    return render_template('index.html', receitas=receitas)

# Rota pra criar uma nova receita, aceita GET (mostrar o formulário) e POST (enviar os dados)
@app.route('/nova-receita', methods=['GET', 'POST'])
def nova_receita():
    """
    Exibe um formulário para criar uma nova receita e processa o envio dos dados.
    Demonstra validação de formulários e redirecionamento com parâmetros.
    """
    if request.method == 'POST':
        # Pega os dados que vieram do formulário
        nome_receita = request.form['nome_receita']  # Nome da receita
        ingredientes = request.form['ingredientes']  # Texto com os ingredientes
        modo_preparo = request.form['modo_preparo']  # Texto com o modo de preparo
        
        # Verifica se algum campo está vazio (validação simples)
        if not nome_receita or not ingredientes or not modo_preparo:
            # Mostra uma mensagem de erro pro usuário usando flash
            flash('Por favor, preencha todos os campos!', 'danger')
            # Volta pro formulário pra ele tentar de novo
            return render_template('receita.html')
        
        # Salva a receita na lista receitas como um dicionário
        receitas.append({
            'nome': nome_receita.strip(),  # Remove espaços extras no nome
            'ingredientes': [i.strip() for i in ingredientes.split('\n') if i.strip()],  # Divide por linhas e remove espaços
            'modo_preparo': modo_preparo.strip()  # Remove espaços extras no modo de preparo
        })
        
        # Redireciona pra página de receita criada, passando os dados pela URL
        return redirect(url_for('receita_criada', 
                              nome_receita=nome_receita, 
                              ingredientes=ingredientes, 
                              modo_preparo=modo_preparo))
    
    # Se for GET, só mostra o formulário de nova receita
    return render_template('receita.html')

# Rota pra mostrar a receita recém-criada
@app.route('/receita-criada')
def receita_criada():
    """
    Exibe a receita criada com os dados enviados pelo formulário.
    """
    # Pega os dados passados pela URL (query string)
    nome_receita = request.args.get('nome_receita', '')  # Nome, com valor padrão vazio
    ingredientes = request.args.get('ingredientes', '')  # Ingredientes, com valor padrão vazio
    modo_preparo = request.args.get('modo_preparo', '')  # Modo de preparo, com valor padrão vazio
    
    # Renderiza o template receita_criada.html com os dados
    return render_template('receita_criada.html', 
                         nome_receita=nome_receita, 
                         ingredientes=ingredientes, 
                         modo_preparo=modo_preparo)

# Nova rota pra mostrar os detalhes de uma receita específica
@app.route('/receita/<int:index>')
def receita_detalhe(index):
    """
    Exibe os detalhes de uma receita com base no índice na lista de receitas.
    """
    # Verifica se o índice é válido
    if index < 0 or index >= len(receitas):
        # Se o índice for inválido, mostra uma mensagem de erro e volta pra página inicial
        flash('Receita não encontrada!', 'danger')
        return redirect(url_for('index'))
    
    # Pega a receita pelo índice
    receita = receitas[index]
    # Renderiza o template de detalhes com a receita
    return render_template('receita_detalhe.html', receita=receita, index=index)

# ---- Executa a aplicação ----
if __name__ == '__main__':
    # Roda o servidor Flask no modo debug (mostra erros detalhados se algo der errado)
    app.run(debug=True)