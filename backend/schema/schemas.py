from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class Ticket(BaseModel):
    name: Optional[str]
    source: Optional[str]
    destination: Optional[str]
    date: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    vehicle_type: Optional[str]
    vehicle_name: Optional[str]
    travel_class: Optional[str]
