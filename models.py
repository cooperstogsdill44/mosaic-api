"""
models.py

Database schema using SQLAlchemy (works with PostgreSQL/Supabase).
This turns the node/edge concept from auto_connections.py into
actual database tables that can be queried and stored long-term -
this is what "Progress Tracking" (Phase 6) will read from.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timezone

Base = declarative_base()


class Assessment(Base):
    """One scan/assessment session - lets a user compare over time."""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    exposure_score = Column(Float, nullable=False)

    nodes = relationship("Node", back_populates="assessment", cascade="all, delete-orphan")
    edges = relationship("Edge", back_populates="assessment", cascade="all, delete-orphan")


class Node(Base):
    """One piece of information (a field) submitted in an assessment."""
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    field_name = Column(String, nullable=False)   # e.g. "username"
    field_value = Column(String, nullable=False)  # e.g. "starlight_j22"

    assessment = relationship("Assessment", back_populates="nodes")


class Edge(Base):
    """A detected connection between two nodes in the same assessment."""
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    field_a = Column(String, nullable=False)
    field_b = Column(String, nullable=False)
    connection_type = Column(String, nullable=False)  # "exact_match" / "partial_match"
    reason = Column(String, nullable=False)

    assessment = relationship("Assessment", back_populates="edges")


if __name__ == "__main__":
    # SQLite here just to prove the schema is valid and runnable;
    # in production this connection string points at Supabase/Postgres.
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # write one synthetic assessment, matching the earlier examples
    assessment = Assessment(exposure_score=55.0)
    assessment.nodes = [
        Node(field_name="username", field_value="starlight_j22"),
        Node(field_name="school", field_value="Lincoln High School"),
    ]
    assessment.edges = [
        Edge(field_a="username", field_b="instagram",
             connection_type="partial_match",
             reason="'username' appears to be reused inside 'instagram'.")
    ]
    session.add(assessment)
    session.commit()

    print("Tables created:", list(Base.metadata.tables.keys()))
    saved = session.query(Assessment).first()
    print(f"\nSaved assessment #{saved.id} | score: {saved.exposure_score}")
    print(f"  nodes: {[(n.field_name, n.field_value) for n in saved.nodes]}")
    print(f"  edges: {[(e.field_a, e.field_b, e.connection_type) for e in saved.edges]}")
