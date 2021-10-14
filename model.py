from exts import db


class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        return fields


class User(db.Model, EntityBase):
    __tablename__ = 'tp_user'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    head = db.Column(db.String(100))
    nickName = db.Column(db.String(100))
    status = db.Column(db.Date)

