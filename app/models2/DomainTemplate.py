from app import db
from ..lib import utils
from ..lib.log import logger
from ..models import logging

class DomainTemplate(db.Model):
    __tablename__ = "domain_template"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.String(255))
    records = db.relationship('DomainTemplateRecord', back_populates='template', cascade="all, delete-orphan")
    
    def __repr__(self):
        return '<DomainTemplate %s>' % self.name
   
    def __init__(self,id=None,name=None,description=None):
        self.id = id
        self.name = name
        self.description = description
        
    def __init__(self,name=None,description=None):
        self.id = None
        self.name = name
        self.description = description
        
    def replace_records(self, records):
        try:
            self.records = []
            for record in records:
                self.records.append(record)
            db.session.commit()
            return {'status': 'ok', 'msg': 'Template records have been modified'}
        except Exception, e:
            logging.error('Cannot create template records' + str(e))
            db.session.rollback()
            return {'status': 'error', 'msg': 'Can not create template records'}
        
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {'status': 'ok', 'msg': 'Template has been created'}
        except Exception, e:
            logging.error('Can not update domain template table.' + str(e))
            db.session.rollback()
            return {'status': 'error', 'msg': 'Can not update domain template table'}
        
    def delete_template(self):
        try:
            self.records = []
            db.session.delete(self)
            db.session.commit()
            return {'status': 'ok', 'msg': 'Template has been deleted'}
        except Exception, e:
            logging.error('Can not delete domain template.' + str(e))
            db.session.rollback()
            return {'status': 'error', 'msg': 'Can not delete domain template'}
            