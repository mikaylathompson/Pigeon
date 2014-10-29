from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    passhash = db.Column(db.String(512))
    publickey = db.Column(db.String(1024))
    privatekey = db.Column(db.String(1024))
    recMessages = db.relationship('Message', backref='receivedMessages', lazy='dynamic')
    friendships = db.relationship('Friend', backref='friendships', lazy='dynamic')
    
    def __repr__(self):
        return '<User %r>'%(self.name)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(8000))
    sent = db.Column(db.DateTime)
    encryp = db.Column(db.Boolean)
    read = db.Column(db.Boolean)

    destID = db.Column(db.Integer, db.ForeignKey('user.id'))

    originName = db.Column(db.String(64))
    #originID = db.Column(db.Integer, db.ForeignKey('user.id'))
    #sender = db.relationship('User', foreign_keys='Message.originID')

    def __repr__(self):
        return '<Message: %r->%r@%r>'%(self.originID, self.destID, self.sent)

class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    ownerID = db.Column(db.Integer, db.ForeignKey('user.id'))
    friendName = db.Column(db.String(64))
    #friendID = db.Column(db.Integer, db.ForeignKey('user.id'))
    #friend = db.relationship('User', foreign_keys='Friend.friendID')
    idverified = db.Column(db.Boolean)

    def __repr__(self):
        return '<Friend %r of %r>'%(self.friendID, self.ownerID)

