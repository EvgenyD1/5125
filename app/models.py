import datetime

from config import PG_DSN
from sqlalchemy import DateTime, Integer, Float, String, func
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Adv(Base):

    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    creator: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    @property
    def dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "creator": self.creator,
            "created_at": self.created_at.isoformat(),
        }


ORM_OBJECT = Adv
ORM_CLS = type[Adv]
