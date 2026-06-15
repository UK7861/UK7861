from pydantic import BaseModel
from typing import List, Optional

class BranchBase(BaseModel):
    branch_name: str
    business_address: str
    latitude: float
    longitude: float

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True

class TenantBase(BaseModel):
    company_name: str
    email: str
    business_number: str
    industry_type: str

class TenantCreate(TenantBase):
    password: str
    # Fields for the initial branch during consolidated onboarding
    initial_branch_name: str
    initial_business_address: str
    initial_latitude: float
    initial_longitude: float

class TenantLogin(BaseModel):
    email: str
    password: str

class Tenant(TenantBase):
    id: int
    branches: List[Branch] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    tenant_id: int
    company_name: str
