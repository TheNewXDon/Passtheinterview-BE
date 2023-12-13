from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import csv


DATABASE_URL = "mysql+mysqlconnector://root:2498@localhost/quiz"
engine = create_engine(DATABASE_URL)


Base = declarative_base()

class Question(Base):
    __tablename__ = "questions_answers"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(length=1000), index=True)
    #category = Column(String)
    #type = Column(String)
    #options = Column(Text)  # Puoi utilizzare JSON al posto di Text se le opzioni sono strutturate
    correct_answer = Column(String(length=10000))
    #difficulty = Column(String)
    #explanation = Column(Text)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=25))
    email = Column(String(length=25))
    password = Column(String(length=25))

class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) 
    questions = Column(Text)
    answers = Column(Text)
    score = Column(Integer)
    
#class QuizQuestionAssociation(Base):
#    __tablename__ = 'quiz_question_association'
#
#    quiz_id = Column(Integer, ForeignKey('quiz.id'), primary_key=True)
#    question_id = Column(Integer, ForeignKey('questions_answers.id'), primary_key=True)

Base.metadata.create_all(bind=engine)

def populate_questions():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Leggi il file CSV e inserisci le domande nel database
    with open('./venv/domande_formattate.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Salta la riga dell'intestazione

        for row in csv_reader:
            print(row)
            question = Question(
                id=row[0],
                question=row[1],
                correct_answer=row[2],
            )
            db.add(question)

    db.commit()
    db.close()

#populate_questions()

Session = sessionmaker(bind=engine)
session = Session()

def get_random_questions(number_of_questions=15):
    # Ottieni il numero specificato di domande casuali dal database
    random_questions = session.query(Question).order_by(func.rand()).limit(number_of_questions).all()
    

    return random_questions

def create_quiz(user_id):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    random_questions = get_random_questions(15)
    quiz_questions = ""
    quiz_answers = ""
    for question in random_questions:
        quiz_questions += question.question + ";"
        quiz_answers += question.correct_answer + ";"
        print(question.question)
    quiz = Quiz(user_id=user_id, questions=quiz_questions, answers=quiz_answers)
    db.add(quiz)
    db.commit()
    db.close()