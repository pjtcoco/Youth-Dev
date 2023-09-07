from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from enum import Enum



db = SQLAlchemy()

class Mentor(db.Model):
    __tablename__ = 'mentor'

    mentor_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    github_link = Column(String(255))
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    organization = Column(String(255))
    images = Column(Text)

    __table_args__ = (
       UniqueConstraint('first_name', 'last_name', 'phone_number', 'email', name='uq_mentor_name'),
    )

    # def __repr__(self):
    #     return f"<Mentor(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"



class Mentee(db.Model):
    __tablename__ = 'mentee'

    mentee_id = Column(Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    organization = db.Column(db.String(255))
    age = db.Column(db.Integer, nullable=False)
    education_level = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    program_studied = db.Column(db.String(255), nullable=False)
    images = db.Column(db.Text)
    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'phone_number', 'email', name='uq_mentee_name'),
    )

    # def __repr__(self):
    #     return f"<Mentee(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"


class SysAdmin(db.Model):
    __tablename__ = 'sysadmin'

    admin_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

class ProjectStatus(Enum):
    NOT_STARTED = 'Not started'
    BLOCKED = 'Blocked'
    REOPENED = 'Reopened'
    IN_PROGRESS = 'Inprogress'

class ProjectCategory(Enum):
    WEB_DEVELOPMENT = 'Web Development'
    MOBILE_DEVELOPMENT = 'Mobile Development'
    MACHINE_LEARNING = 'Machine Learning'
    ARTIFICIAL_INTELLIGENCE = 'Artificial Intelligence'
    NETWORKING = 'Networking'

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False, unique=True)
    project_status = db.Column(db.Enum(ProjectStatus), nullable=False)
    project_github = db.Column(db.String(500), nullable=False)
    workers = db.Column(db.Integer, nullable=False)
    project_category = db.Column(db.Enum(ProjectCategory), nullable=False)
    project_description = db.Column(db.String, nullable=False)
    created_by = db.column(db.String(200))
    date_added = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    