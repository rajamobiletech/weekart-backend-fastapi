from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Integer,  server_default='0', nullable=True)
    image_url = Column(String, nullable=True)
    discount = Column(Integer,  server_default='0', nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    shippername = Column(String)
    owner = relationship("User")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True,  nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), primary_key=True)