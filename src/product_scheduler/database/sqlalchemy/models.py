from typing import Optional

from sqlalchemy import (
    Integer,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __table_args__ = {"schema": "scheduler"}


class ResourceKind(Base):
    __tablename__ = "resource_kinds"
    resource_kind_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )
    resource_kind_name: Mapped[str] = mapped_column(String(16), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint(resource_kind_id),
        UniqueConstraint(resource_kind_name),
    )


class Resource(Base):
    __tablename__ = "resources"
    resource_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )
    resource_name: Mapped[str] = mapped_column(String(16), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint(resource_id),
        UniqueConstraint(resource_name),
    )


class Job(Base):
    __tablename__ = "jobs"
    job_id: Mapped[int] = mapped_column(Integer, autoincrement=True, nullable=False)
    job_name: Mapped[str] = mapped_column(String(16), nullable=False)
    __table_args__ = (PrimaryKeyConstraint(job_id), UniqueConstraint(job_name))
    operations: Mapped[list["Operation"]] = relationship(back_populates="jobs")


class Operation(Base):
    __tablename__ = "operations"
    operation_id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, nullable=False
    )
    operation_name: Mapped[str] = mapped_column(String(16), nullable=False)
    job_id: Mapped[int] = mapped_column(
        ForeignKey(Job.job_id, ondelete="CASCADE"), nullable=False
    )
    sequence_index: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_operation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("operations.operation_id"), nullable=False
    )
    __table_args__ = (
        PrimaryKeyConstraint(operation_id),
        UniqueConstraint(job_id, sequence_index),
    )
    jobs: Mapped[list[Job]] = relationship(back_populates="operations")
    parent_operation: Mapped[Optional["Operation"]] = relationship(
        "Operation", remote_side=[operation_id], back_populates="chile_operations"
    )
    child_operations: Mapped[list["Operation"]] = relationship(
        "Operation", back_populates="parent_operation"
    )
