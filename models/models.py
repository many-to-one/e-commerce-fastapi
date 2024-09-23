from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum
# from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import text, false
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=false(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    is_admin = Column(Boolean, server_default=false(), nullable=False)
    access_token = Column(String, nullable=True)

    # New column for role
    # role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")

    # Relationship with carts
    carts = relationship("Cart", back_populates="user", lazy="selectin")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount = Column(Float, nullable=False)

    # Relationship with user
    user = relationship("User", back_populates="carts")

    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="cart", lazy="selectin")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationship with cart and product
    cart = relationship("Cart", back_populates="cart_items", lazy="selectin")
    product = relationship("Product", back_populates="cart_items", lazy="selectin")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with products through subcategories
    products = relationship("Product", back_populates="category", lazy="selectin", cascade="all, delete")

    # Relationship with subcategories
    subcategories = relationship("Subcategory", back_populates="category", lazy="selectin", cascade="all, delete")


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with category
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="subcategories", lazy="selectin")

    # Relationship with products
    products = relationship("Product", back_populates="subcategory", lazy="selectin", cascade="all, delete")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    discount_percentage = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    stock = Column(Integer, nullable=False)
    brand = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)
    images = Column(ARRAY(String), nullable=True)
    is_published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # Relationship with category
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="products", lazy="selectin")

    # Relationship with subcategory
    subcategory_id = Column(Integer, ForeignKey("subcategories.id", ondelete="CASCADE"), nullable=True)
    subcategory = relationship("Subcategory", back_populates="products", lazy="selectin")

    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="product", lazy="selectin")



# class Category(Base):
#     __tablename__ = "categories"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)

#     # Relationship with products
#     products = relationship("Product", back_populates="category", lazy="selectin",  cascade="all, delete")


# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=True)
#     price = Column(Float, nullable=False)
#     discount_percentage = Column(Float, nullable=True)
#     rating = Column(Float, nullable=True)
#     stock = Column(Integer, nullable=False)
#     brand = Column(String, nullable=True)
#     thumbnail = Column(String, nullable=True)
#     images = Column(ARRAY(String), nullable=True)
#     is_published = Column(Boolean, server_default="True", nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

#     # Relationship with category
#     category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
#     category = relationship("Category", back_populates="products", lazy="selectin")

#     # Relationship with cart items
#     cart_items = relationship("CartItem", back_populates="product", lazy="selectin")
