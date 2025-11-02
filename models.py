from atexit import register
from datetime import datetime

from sqlalchemy import create_engine, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

from const import StatusChoices, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=True)

    @property
    def json(self):
        return {
            "id": self.id,
            "username": self.username,
        }

class Ticket(Base):
    __tablename__ = 'tickets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String)
    status: Mapped[StatusChoices] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[User] = mapped_column(ForeignKey(User.id), nullable=False)

    @property
    def json(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "user": self.user,
        }


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
register(engine.dispose)






