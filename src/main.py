from typing import List

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

Base = declarative_base()
class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    tag = Column(String)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id"))
    interaction: Mapped["Interaction"] = relationship(back_populates="tags")

# Define a custom class
class Interaction(Base):

    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    topic = Column(String)
    tags: Mapped[List["Tag"]] = relationship(
        back_populates="interaction",
        cascade="all, delete-orphan")
    summary = Column(String)
    Details = Column(String)

    def __repr__(self):
        return f"<MimsObject(topic='{self.topic}', summary='{self.summary}')>"

# Create an engine to connect to your database
engine = create_engine('sqlite:///mydatabase.db')

# Create a base class for your models
Base.metadata.create_all(engine)
session = Session(engine)


interaction = Interaction(
    topic="test",
    summary="test sumt",
    Details="the deets",
    tags=[
        Tag(tag="tag1"),
        Tag(tag="tag2")
    ]
    )

session.add(interaction)
session.commit()

# Retrieve a user with their addresses
retrieved_user = session.query(Interaction).filter_by(topic="test").first()
print(retrieved_user)
for i in retrieved_user.tags:
    print(i.tag)

