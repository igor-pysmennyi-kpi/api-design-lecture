from typing import TypeVar, Generic, List

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


T = TypeVar('T')
class Page(Generic[T], db.Model):
    __tablename__ = 'pages'

    id_col = db.Column(db.VARCHAR(12), primary_key=True)
    size_col = db.Column(db.Integer)
    page_col = db.Column(db.Integer)
    total_pages_col = db.Column(db.Integer)
    content_col = db.Column(db.String(120))  

    def __init__(self, size: int, page: int, total_pages: int, content: List[T]):
        self.size = size
        self.page = page
        self.total_pages = total_pages
        self.content = content

    def print_content(self):
        print(self.content)
        
    def to_json(self):
        return {
            'size': self.size,
            'page': self.page,
            'total_pages': self.total_pages,
            'content': [item.__dict__ for item in self.content]
        }

    @property
    def serialize(self):
        return {
            'id': Page.id_col,
            'size': Page.size_col,
            'page': Page.page_col,
            'total_pages': Page.total_pages_col,
            'content': Page.content_col
        }
