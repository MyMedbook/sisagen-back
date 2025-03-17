# api/models/base.py
from mongoengine import (Document, IntField, DateTimeField, EnumField, StringField, 
                         EmbeddedDocument, EmbeddedDocumentField)
from datetime import datetime
from enum import Enum

common_indices = [
            'paziente_id',
            'operatore_id',
            'datamanager_id',
            'structure.pk',
            'created_at',
            'updated_at'
        ]

class Status(str, Enum):
    DRAFT = "draft"
    COMPLETE = "complete"
    ARCHIVED = "archived"

class Structure(EmbeddedDocument):

    pk = IntField(required=True)
    name = StringField()
    max_members = StringField()
    max_affiliates = StringField()
    label = StringField()
    mobile_number = StringField()
    phone_number = StringField()
    code_type = StringField()
    created = DateTimeField()
    updated = DateTimeField()

class BaseDocument(Document):
    """Base document class with common fields and metadata"""
    paziente_id = IntField(required=True)
    operatore_id = IntField(required=True)
    datamanager_id = IntField()
    structure = EmbeddedDocumentField(Structure, required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    meta = {
        'abstract': True,
        'indexes': common_indices
    }

    def save(self, *args, **kwargs):
        """Update updated_at timestamp on every save"""
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def validate_patient(self):
        """Validate paziente_id"""
        if self.paziente_id <= 0:
            raise ValueError("paziente_id must be positive")

    def clean(self):
        """Perform document validation before saving"""
        self.validate_patient()
        super().clean()
