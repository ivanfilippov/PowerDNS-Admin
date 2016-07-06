from app import db
from ..lib import utils
from ..lib.log import logger
from ..models import logging

class DomainTemplate(db.Model):
    __tablename__ = "domain_template"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.String(255))
    records = db.relationship('DomainTemplateRecord', back_populates='template')
    
    def __repr__(self):
        return '<DomainTemplate %s>' % self.name
    
    def init(self,id=None,name=None,description=None):
        self.id = id
        self.name = name
        self.description = description
        
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'status': 'ok', 'msg': 'Template has been created'}
        except Exception, e:
            logging.error('Can not update domain template table.' + str(e))
            db.session.rollback()
            return {'status': 'error', 'msg': 'Can not update domain template table'}