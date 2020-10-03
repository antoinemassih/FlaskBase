from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref
from flask_potion.routes import Relation, ItemRoute, Route
from flask_potion import ModelResource, fields, Api, Resource
from resources.nonDB import NoDBResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Monkeyhero69@trendchart.cu0jwgiytj6k.us-east-1.rds.amazonaws.com:5432/postgres"
db = SQLAlchemy(app)


class Author(db.Model):
    __tablename__ = 'Author'
    schema = 'public'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name'),  # unique constraint added here
    )


class Book(db.Model):
    __tablename__ = 'Book'
    schema = 'public'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id), nullable=False)

    title = db.Column(db.String(), nullable=False)
    year_published = db.Column(db.Integer)

    author = db.relationship(Author, backref=backref('books', lazy='dynamic'))
    rating = db.Column(db.Integer, default=5)


db.init_app(app)
db.create_all()


class BookResource(ModelResource):
    class Meta:
        model = Book
        excluded_fields = ['rating']

    @ItemRoute.GET('/rating')
    def rating(self, book) -> fields.Integer():
        return book.rating

    @rating.POST
    def rate(self, book, value: fields.Integer(minimum=1, maximum=10)) -> fields.Integer():
        self.manager.update(book, {"rating": value})
        return value

    @ItemRoute.GET
    def is_recent(self, book) -> fields.Boolean():
        return datetime.date.today().year <= book.year_published + 10

    @Route.GET
    def genres(self) -> fields.List(fields.String, description="A list of genres"):
        return ['biography', 'history', 'essay', 'law', 'philosophy']

    class Schema:
        author = fields.ToOne('author')


class AuthorResource(ModelResource):
    books = Relation('book')

    class Meta:
        model = Author
        natural_key = ('first_name', 'last_name')  # natural key declaration added here


api = Api(app)
api.add_resource(BookResource)
api.add_resource(NoDBResource)
api.add_resource(AuthorResource)

if __name__ == '__main__':
    app.run()
