from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __table_args__ = {"schema": "scheduler"}


class ResourceKind(Base):
    __tablename__ = "resource_kinds"
    resource_kind_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )


class Resource(Base):
    __tablename__ = "resources"
    resource_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )


class Job(Base):
    __tablename__ = "jobs"
    job_id: Mapped[int] = mapped_column(Integer, autoincrement=True, nullable=False)
    job_name: Mapped[String] = mapped_column(String(16), nullable=False)


class Operation(Base):
    __tablename__ = "operations"
    operation_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )
    operation_name: Mapped[str] = mapped_column(String(16), nullable=False)
    job_id: Mapped[int] = mapped_column(ForeignKey(), nullable=False)
    suquence_index: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_operation_id: Mapped[int] = mapped_column(ForeignKey(), nullable=False)
