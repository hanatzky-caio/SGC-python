from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def configurar_banco(app):
    """
    Função responsável pela configuração e inicialização do banco de dados

    Args:
        app (Flask) - applicação já incializada com Flask

    returns:

        não há retorno, apenas confirmação de inicialização do banco de dados
    """

    
    #Define o URI do host para conexão com o banco
    #Nesse caso está sendo utilizado o Sqlite e criação do banco local

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalogo.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    print('Banco de dados criado com sucesso')