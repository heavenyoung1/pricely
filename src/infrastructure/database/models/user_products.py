class ORMUserProducts(Base):
    __tablename__ = "user_products"

    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )  # Идентификатор пользователя, внешний ключ

    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )  # Идентификатор продукта, внешний ключ
