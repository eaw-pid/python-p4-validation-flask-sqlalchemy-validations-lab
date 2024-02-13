from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    #Add validators 
    @validates('name')
    ##all authors must have name and no two authors can have the same name
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Author must have a name')
        
        existing_author = Author.query.filter(Author.name == name).first()
      
        if existing_author:
            raise ValueError('Author already exists')
        
        return name

    
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if  len(number) != 10 or not number.isdigit():
            raise ValueError('Phone number must be 10 digits')
        return number
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content has to be less than or equal to 250 characters long.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary character maximum is 250')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError('Category must be Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not title:
            raise ValueError('Post must include a Title.')
        if not any(substring in title for substring in clickbait):
            raise ValueError('Title must include Clickbait word')
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
