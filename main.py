from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

#Criar tabela eu crio uma classe
class Artista(Base):
    __tablename__ = "artistas"

    #Como criar colunas
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column( Integer, nullable=False)
    nacionalidade = Column(String(100), nullable=False)
    nome_artistico = Column(String(100), nullable=False)

    albuns = relationship("Album", back_populates="artistas")

    #Função de imprimir
    def __repr__(self):
        return f"ALBUM: ID = {self.id} - NOME = {self.nome}"


#Criar a class Funcionario com as colunas: id, nome, cargo, salario
class Album(Base):
    __tablename__ = "albuns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    lancamento = Column(Integer, nullable=False)
    quantidade_musicas = Column(Integer, nullable=False)
    faixa_principal = Column(String(100), nullable=False)

    #ForeignKey é o que eu criar o vínuclo no banco
    artistas_id = Column(Integer, ForeignKey("artistas.id"))

    #Relacionamento
    artistas = relationship("Artista", back_populates="albuns")

    def __repr__(self):
        return f"ALBUM: ID = {self.id} - NOME = {self.nome} - LANÇAMENTO = {self.lancamento} - QUANTIDADE DE MUSICAS = {self.quantidade_musicas} - FAIXA PRINCIPAL = {self.faixa_principal}"
   

engine = create_engine("sqlite:///Entreterimento.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#Função para cadastrar os departamentos
def cadastrar_artista():
    nome_artista = input("Digite o nome real do artista: ").strip().capitalize()
    idade = int(input("Digite a idade do artista: "))
    nacionalidade = input("Digite a nacionalidade do artista: ").strip().capitalize()
    nome_artistico = input("Digite o nome artistico: ").strip().capitalize()

    with Session() as session:
        try:
            artista = Artista(nome=nome_artista, idade=idade, nacionalidade=nacionalidade,nome_artistico=nome_artistico)
            session.add(artista)
            session.commit()
            print("Artista cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
    
def cadastrar_album():
    nome_album = input("Digite o nome do álbum: ").strip().capitalize()
    lancamento_album = input(f"Digite o lançamento do álbum {nome_album}: ").capitalize()
    qtd_musicas = int(input(f"Digite a quantidade de músicas do álbum {nome_album}: "))
    faixa_principal = input(f"Digite a faixa principal do álbum {nome_album}: ").capitalize()

    buscar_artista = input(f"Digite o nome do artistas do álbum {nome_album}: ").strip().capitalize()

    with Session() as session:
        try:
            #Como buscar um valor no banco usando sqlalchemy
            albuns = session.query(Artista).filter_by(nome=buscar_artista).first()
            if buscar_artista == None:
                print("Não encontrei nenhum artista com esse nome.")
                return
            else:
                albuns = Album(nome=nome_album, lancamento=lancamento_album, quantidade_musicas=qtd_musicas, faixa_principal=faixa_principal)
                session.add(albuns)
                session.commit()
                print(f"Álbum cadastrado com sucesso!")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")
