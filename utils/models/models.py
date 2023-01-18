from sqlalchemy import Column, BIGINT, VARCHAR, BOOLEAN, INT, ForeignKey

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    is_active = Column(BOOLEAN, default=True)


class Question(Base):
    __tablename__ = 'questions'

    question = Column(VARCHAR(1024), nullable=False)
    media_id = Column(VARCHAR(512), nullable=True)


class QuestionAnswer(Base):
    __tablename__ = 'question_answers'

    answer = Column(VARCHAR(64), nullable=False)
    question_id = Column(INT, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
