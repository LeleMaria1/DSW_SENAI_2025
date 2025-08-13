from flask import Flask, render_template, request

app = Flask(__name__)


#Rota para o endereço /index
@app.route('/index')
def exibir_index():
    return render_template('index.html')


#Rota para o endereço /sucesso
@app.route('/sucesso')
def exibir_sucesso():
    return render_template('/sucesso.html')

# Certifica-se que o aplicativo seja executado
if __name__ == '__main__':
    app.run(debug=True)
