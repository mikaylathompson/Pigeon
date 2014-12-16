from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    passhash = db.Column(db.String(512))
    publickey = db.Column(db.String(1024))
    privatekey = db.Column(db.String(1024))

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.name)
    def __repr__(self):
        return '<User %r>'%(self.name)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(8000))
    sent = db.Column(db.DateTime)
    read = db.Column(db.Boolean)
    destName = db.Column(db.String(64))
    originName = db.Column(db.String(64))

    def json(self):
        j = {}
        j['id'] = self.id
        j['content'] = self.text
        j['sent'] = self.sent
        j['read'] = self.read
        j['destName'] = self.destName
        j['originName'] = self.originName
        return j

    def __repr__(self):
        return '<Message: %r->%r@%r>'%(self.originID, self.destID, self.sent)

