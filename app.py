from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, configurar_banco
from models import Produto

app = Flask(__name__)

app.config['SECRET_KEY'] = 'caio-chave-flash'

configurar_banco(app)

@app.route('/')
def index():

    try:
        produtos = Produto.query.order_by(Produto.nome).all() 
       
        return render_template('index.html', produtos=produtos)
    except Exception as erro:
        print(f'Erro ao listar {erro}')
        flash('Erro ao carregar lista de produtos', 'danger')
        return render_template('index.html', produtos=[])


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():

    if request.method == 'GET':
        return render_template('adicionar.html')

    try: 
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '').strip()
        quantidade = request.form.get('quantidade', '').strip()

        if not nome:
            flash('O nome do produto é obrigatório', 'danger')
            return render_template('adicionar.html', nome=nome, descricao=descricao, preco=preco, 
                                   quantidade=quantidade)

        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)

        db.session.add(novo_produto)
        db.session.commit()

        flash(f'Produto {nome} adicionado com sucesso')

        return redirect(url_for('index'))
    
    except Exception as erro:
        print(f'Erro ao adicionar: {erro}')
        flash('Erro ao adicionar o produto')
        return render_template('adicionar.html')
    

@app.route('/deletar/<int:id>')
def deletar(id):

    try:
        produto = Produto.query.get_or_404(id)
        nome_produto = produto.nome

        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto {nome_produto} removido com sucesso', 'success')
    except Exception as erro:
        db.session.rollback()
        print(f'Erro ao deletar: {erro}')

        flash(f'Erro ao remover produto. Tente novamente', 'danger')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    produto = Produto.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('editar.html', produto=produto)

    try:
        nome = request.form.get('nome', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco', '').strip()
        quantidade = request.form.get('quantidade', '').strip()

        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.quantidade = quantidade

        db.session.commit()

        flash(f'Produto {nome} atualizado com sucesso', 'success')
        return redirect(url_for('index'))
    except Exception as erro:
        db.session.rollback()
        print(f'Erro ao editar: {erro}')
        flash(f'Erro ao atualizar produto. Tente mais tarde')

        return render_template(url_for('editar.html', produto=produto))
    
    
if __name__ == '__main__':
    app.run(debug=True)