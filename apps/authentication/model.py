from app import db


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))

    def save(self):
        db.session.add(self)
        db.session.commit()
