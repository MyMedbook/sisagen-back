# api/models/pedigree.py
from mongoengine import (
    Document, EmbeddedDocument, EmbeddedDocumentField, 
    StringField, BooleanField, IntField, ListField,
    DateTimeField, EnumField
)
from datetime import datetime
from enum import Enum

# Enums for Pedigree
class Severita(str, Enum):
    LIEVE = "lieve"
    SEVERA = "severa"

class Device(str, Enum):
    NO = "no"
    PM = "pm"
    ICD = "icd"
    CRT = "crt"

class Status(str, Enum):
    DRAFT = "draft"
    COMPLETE = "complete"
    ARCHIVED = "archived"

# Base Document
class BaseDocument(Document):
    """Base document class with common fields"""
    paziente_id = IntField(required=True)
    operatore_id = IntField(required=True)
    status = EnumField(Status, default=Status.DRAFT)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'abstract': True,
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at'
        ]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def validate_patient(self):
        if self.paziente_id <= 0:
            raise ValueError("paziente_id must be positive")

    def clean(self):
        self.validate_patient()
        super().clean()

# Base Embedded Document for Family Members
class BaseFamilyMember(EmbeddedDocument):
    """Base embedded document for all family member types"""
    stessa_malattia = BooleanField(required=True)
    eta_esordio = IntField(min_value=0)
    severita = EnumField(Severita)
    morte_improvvisa = BooleanField(required=True)
    eta_morte = IntField(min_value=0)
    device = EnumField(Device, default=Device.NO)

    meta = {'allow_inheritance': True}

# Specific Family Member Types
class DirectFamilyMember(BaseFamilyMember):
    """For parents and grandparents"""
    pass

class NumberedFamilyMember(BaseFamilyMember):
    """For siblings and children"""
    numero = IntField(required=True, min_value=1)

# Main Pedigree Document
class Pedigree(BaseDocument):
    """Main pedigree document containing family history"""
    padre = EmbeddedDocumentField(DirectFamilyMember)
    madre = EmbeddedDocumentField(DirectFamilyMember)
    nonno_paterno = EmbeddedDocumentField(DirectFamilyMember)
    nonna_paterna = EmbeddedDocumentField(DirectFamilyMember)
    nonno_materno = EmbeddedDocumentField(DirectFamilyMember)
    nonna_materna = EmbeddedDocumentField(DirectFamilyMember)
    fratelli = ListField(EmbeddedDocumentField(NumberedFamilyMember))
    figli = ListField(EmbeddedDocumentField(NumberedFamilyMember))

    meta = {
        'collection': 'pedigree',
        'indexes': [
            'paziente_id',
            'operatore_id',
            'created_at',
            ('paziente_id', 'status')
        ]
    }

    def clean(self):
        """Validate the document before saving"""
        super().clean()
        
        # Validate that numbered family members have unique numbers
        self._validate_numbered_members('fratelli')
        self._validate_numbered_members('figli')

    def _validate_numbered_members(self, field_name):
        """Helper method to validate numbered family members"""
        members = getattr(self, field_name, [])
        if members:
            numbers = [m.numero for m in members]
            if len(numbers) != len(set(numbers)):
                raise ValueError(f"Duplicate numbers found in {field_name}")