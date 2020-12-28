import datetime

from app import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name

    @property
    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

    @property
    def serializer(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'pub_date': self.pub_date.strftime("%x %X %p"),
            'category': self.category.serializer,
            'user_id': self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
