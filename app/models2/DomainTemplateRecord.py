from app import db
from ..lib import utils
from ..lib.log import logger


class DomainTemplateRecord(db.Model):
    __tablename__ = "domain_template_record"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(64))
    ttl = db.Column(db.Integer)
    data = db.Column(db.String(255))
    status = db.Column(db.Boolean) 
    template_id = db.Column(db.Integer, db.ForeignKey('domain_template.id'))
    template = db.relationship('DomainTemplate', back_populates='records')

    def __repr__(self):
        return '<DomainTemplateRecord %i>' % self.id
    
    def init(self,id=None,name=None,type=None,ttl=None,data=None,status=None):
        self.id = id
        self.name = name
        self.type = type
        self.ttl = ttl
        self.data = data
        self.status = status
    
    def apply(self):
        try:
            db.session.commit()
        except Exception, e:
            logging.error('Can not update domain template table.' + str(e))
            db.session.rollback()
            return {'status': 'error', 'msg': 'Can not update domain template table'}
                