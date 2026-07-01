from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    in_stock = Column(Boolean)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


new_category = Category(
    name="Electronics",
    description="Electronic devices and accessories"
)

new_product = Product(
    name="PC",
    price=30.00,
    in_stock=True,
    category=new_category
)



session.add(new_category)
session.add(new_product)
session.commit()

db = session.query(Product).first()


# print(db.id, db.name, db.price, db.in_stock)
# print(db.category.name)

products = session.query(Product).all()

for product in products:
    print(
        product.id, '|',
        product.name, '|',
        product.price, '|',
        product.in_stock, '|',
        product.category_id
    )

categories = session.query(Category).all()

for category in categories:
    print(
        category.id,
        category.name,
        category.description
    )

session.close()