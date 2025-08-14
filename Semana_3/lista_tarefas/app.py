from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tarefas = []#Lista para armazenar as tarefas

@app.route('/', methods=['GET', 'POST'])
def exibir_index():
    if request.method == 'POST':
        tarefa_nome = request.form.get('tarefa')
        data_limite = request.form.get('data_limite')

        nova_tarefa = {'nome': tarefa_nome, 'data_limite': data_limite}
        tarefas.append(nova_tarefa)

        return redirect(url_for('exibir_sucesso', tarefa_nome=tarefa_nome))

    return render_template('index.html', tarefas=tarefas)


@app.route('/sucesso')
def exibir_sucesso():
    tarefa_nome = request.args.get('tarefa_nome')
    return render_template('sucesso.html', tarefa_nome=tarefa_nome)


# Certifica-se que o aplicativo seja executado
if __name__ == '__main__':
    app.run(debug=True)