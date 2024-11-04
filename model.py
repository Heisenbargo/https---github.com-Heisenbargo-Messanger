from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Создаем базу и движок SQLAlchemy
Base = declarative_base()
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель пользователя
class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    # Связь с моделью Message для отправленных и полученных сообщений
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")

    def __repr__(self):
        return f"<User {self.username}>"

# Модель сообщений
class Message(Base):
    __tablename__ = "Message"
    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    content = Column(String(), nullable=False)
    timestamp = Column(String, default=datetime.utcnow)

    # Связи с моделью Users для получения данных отправителя и получателя
    sender = relationship("Users", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="received_messages")

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.receiver_id} at {self.timestamp}>"

# Функция для создания и закрытия сессий
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для поиска пользователя в базе данных по имени
def find_user_in_database(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

# Создаем таблицы в базе данных, если их еще нет
Base.metadata.create_all(bind=engine)
