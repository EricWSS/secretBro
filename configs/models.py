from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Base para mapeamento ORM
Base = declarative_base()

class DatabaseConnection:
    def __init__(self):
        # Obtém a URL do banco de dados de uma variável de ambiente ou parâmetro
        self.database_url = "postgresql://postgres.ljqbfkrgogtknhvguksx:Er!c121970@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"
        if not self.database_url:
            raise ValueError("DATABASE_URL is not set")

        # Configura o engine e o Session
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=self.engine)

    def get_session(self):
        """Cria uma nova sessão de banco de dados."""
        try:
            session = self.SessionLocal()
            return session
        except Exception as e:
            print(f"Failed to create database session: {e}")
            raise

    def close_engine(self):
        """Fecha o engine ao encerrar o aplicativo."""
        if self.engine:
            self.engine.dispose()
            print("Database engine closed")

# Inicializar a conexão com o banco de dados
db = DatabaseConnection()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    key_sorteio = Column(String(12), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, user='{self.user}', created_at={self.created_at}, key_sorteio='{self.key_sorteio}')>"


