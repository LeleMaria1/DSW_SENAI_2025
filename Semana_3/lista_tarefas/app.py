from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista simples para armazenar as tarefas.
# Em uma aplicação real, você usaria um banco de dados.
tarefas = []

# Rota principal para a página inicial (index.html)
# Agora ela aceita os métodos GET (para exibir a página) e POST (para receber dados do formulário)
@app.route('/', methods=['GET', 'POST'])
def exibir_index():
    # Se a requisição for do tipo POST, significa que o formulário foi enviado
    if request.method == 'POST':
        # Pega os dados do formulário com base nos nomes dos inputs
        tarefa_nome = request.form.get('tarefa')
        data_limite = request.form.get('data_limite')

        # Adiciona a nova tarefa à lista
        nova_tarefa = {'nome': tarefa_nome, 'data_limite': data_limite}
        tarefas.append(nova_tarefa)

        # Redireciona para a página de sucesso, passando o nome da tarefa como parâmetro
        return redirect(url_for('exibir_sucesso', tarefa_nome=tarefa_nome))

    # Se a requisição for GET, apenas renderiza a página com a lista de tarefas atual
    return render_template('index.html', tarefas=tarefas)


# Rota para a página de sucesso
# Ela agora recebe o nome da tarefa como um argumento da URL
@app.route('/sucesso')
def exibir_sucesso():
    # Pega o nome da tarefa que foi passado na URL
    tarefa_nome = request.args.get('tarefa_nome')
    return render_template('sucesso.html', tarefa_nome=tarefa_nome)


# Certifica-se que o aplicativo seja executado
if __name__ == '__main__':
    app.run(debug=True)