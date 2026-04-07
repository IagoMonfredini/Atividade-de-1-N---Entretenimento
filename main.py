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
    nome_album = Column(String(100), nullable=False)
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
    lancamento_album = int(input(f"Digite o lançamento do álbum {nome_album}: "))
    qtd_musicas = int(input(f"Digite a quantidade de músicas do álbum {nome_album}: "))
    faixa_principal = input(f"Digite a faixa principal do álbum {nome_album}: ").strip().capitalize()

    buscar_artista = input(f"Digite o nome do artista do álbum {nome_album}: ").strip().capitalize()

    with Session() as session:
        try:
            artista = session.query(Artista).filter_by(nome=buscar_artista).first()

            if not artista:
                print("Não encontrei nenhum artista com esse nome.")
                return

            album = Album(
                nome_album=nome_album,
                lancamento=lancamento_album,
                quantidade_musicas=qtd_musicas,
                faixa_principal=faixa_principal,
                artistas=artista
            )

            session.add(album)
            session.commit()
            print("Álbum cadastrado com sucesso!")

        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")

def listar_albuns():
    with Session() as session:
        try:
            albuns = session.query(Album).all()

            if not albuns:
                print("Nenhum álbum encontrado.")
                return

            print()
            for album in albuns:
                print(f"Álbum: {album.nome_album} | Artista: {album.artistas.nome_artistico}")

        except Exception as erro:
            print(f"Ocorreu um erro: {erro}")

def listar_albuns_por_artista():
    buscar_artista = input("Digite o nome do artista: ").strip().capitalize()
    with Session() as session:
        try:
            artista = session.query(Artista).filter_by(nome_artistico=buscar_artista).first()
            if not artista:
                print("Não encontrei nenhum artista com esse nome.")
                return
            print()
            for album in artista.albuns:
                print(f"Álbum: {album.nome_album} | Artista: {artista.nome_artistico}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

def listar_artistas_com_albuns():
    with Session() as session:
        try:
            artistas = session.query(Artista).filter(Artista.albuns.any()).all()
            if not artistas:
                print("Nenhum artista com álbuns cadastrado.")
                return
            print()
            for artista in artistas:
                print(f"Artista: {artista.nome_artistico} | Qtd. de álbuns: {len(artista.albuns)}")
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro: {erro}")

