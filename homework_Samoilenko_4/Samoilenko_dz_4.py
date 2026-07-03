from decimal import Decimal

from sqlalchemy import create_engine, String, Numeric, Boolean, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload


engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")


Base.metadata.create_all(engine)

#1
def add_data(session: Session) -> None:
    electronics = Category(
        name="Electronics",
        description="Gadgets and devices."
    )

    books = Category(
        name="Books",
        description="Printed books and e-books."
    )

    clothing = Category(
        name="Clothing",
        description="Clothing for men and women."
    )

    products = [
        Product(
            name="Smartphone",
            price=Decimal("299.99"),
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Laptop",
            price=Decimal("499.99"),
            in_stock=True,
            category=electronics
        ),
        Product(
            name="Science Fiction Novel",
            price=Decimal("15.99"),
            in_stock=True,
            category=books
        ),
        Product(
            name="Jeans",
            price=Decimal("40.50"),
            in_stock=True,
            category=clothing
        ),
        Product(
            name="T-Shirt",
            price=Decimal("20.00"),
            in_stock=True,
            category=clothing
        ),
    ]

    session.add_all(products)
    session.commit()


def show_all_products(session: Session) -> None:
    products = session.scalars(select(Product)).all()

    print("\nAll products:")

    for product in products:
        print(
            product.id,
            product.name,
            product.price,
            product.in_stock,
            product.category.name
        )


def show_categories_with_products(session: Session) -> None:
    categories = session.scalars(
        select(Category).options(selectinload(Category.products))
    ).all()

    print("\nCategories with products:")

    for category in categories:
        print(f"\nCategory: {category.name}")
        print(f"Description: {category.description}")
        print("Products:")

        for product in category.products:
            print(f"- {product.name}: {product.price}")


def update_smartphone_price(session: Session) -> None:
    product = session.scalars(
        select(Product).where(Product.name == "Smartphone")
    ).first()

    print("\nUpdate product price:")

    if product:
        product.price = Decimal("349.99")
        session.commit()
        print("Price updated")
    else:
        print("Product not found")


def show_smartphone(session: Session) -> None:
    product = session.scalars(
        select(Product).where(Product.name == "Smartphone")
    ).first()

    print("\nUpdated smartphone:")

    if product:
        print(product.id, product.name, product.price)


def count_products_by_category(session: Session) -> None:
    result = session.execute(
        select(
            Category.name,
            func.count(Product.id).label("product_count")
        )
        .join(Product)
        .group_by(Category.id, Category.name)
    ).all()

    print("\nProduct count by category:")

    for category_name, product_count in result:
        print(f"{category_name}: {product_count}")


def show_categories_with_more_than_one_product(session: Session) -> None:
    result = session.execute(
        select(
            Category.name,
            func.count(Product.id).label("product_count")
        )
        .join(Product)
        .group_by(Category.id, Category.name)
        .having(func.count(Product.id) > 1)
    ).all()

    print("\nCategories with more than one product:")

    for category_name, product_count in result:
        print(f"{category_name}: {product_count}")


Base.metadata.create_all(engine)

with Session(engine) as session:
    add_data(session)
    show_all_products(session)
    show_categories_with_products(session)
    update_smartphone_price(session)
    show_smartphone(session)
    count_products_by_category(session)
    show_categories_with_more_than_one_product(session)