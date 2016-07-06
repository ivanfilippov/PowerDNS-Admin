from app import db
from ..lib import utils
from ..lib.log import logger

class DomainTemplateRecord(db.Model):
    __tablename__ = "domain_template_record"
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(64))
    ttl = db.Column(db.Integer)
    data = db.Column(db.String(255))
    status = db.Column(db.Boolean) 
    template_id = db.Column(db.Integer, db.ForeignKey('domain_template.id'))
    template = db.relationship('DomainTemplate', back_populates='records')