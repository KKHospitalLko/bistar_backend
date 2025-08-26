from sqlmodel import SQLModel
from typing import Optional
from pydantic import field_validator

class BedDetailsCreateSchema(SQLModel):
    uhid: Optional[str] = None
    patient_name: str
    department: str
    bed_number: str

class BedDetailsResponseSchema(SQLModel):
    bed_id: Optional[int] = None
    uhid: Optional[str] = None
    patient_name: str
    department: str
    bed_number: str
    status: str