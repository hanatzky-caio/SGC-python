from database import db
from typing import Optional, List, Dict

class Produto(db.Model):

    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True, default='')
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=0)

    def __init__(self, nome: str, descricao: str, preco: float, quantidade:int=0):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.descricao = descricao

    def __repr__(self):
        return f'<Produto: {self.nome}'
    
    def verifica_estoque(self)->bool:
        return self.quantidade > 0
    
    def preco_formatado(self):
        return f'R$ {self.preco:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    
    def valor_total_formatado(self):
        valor_total = self.quantidade * self.preco
        return f'R$ {valor_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    