from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import io
import os
import logging
from gtts import gTTS
from typing import List

from . import models, schemas
from .models import SessionLocal, engine
from .agents.matrix import agent_matrix

# Initialize database
models.Base.metadata.create_all(bind=engine)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PinPointCore")

app = FastAPI(title="Pin Point Core API")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

# Global CORS footprint
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AUTH & ONBOARDING ---

@app.post("/auth/signup", response_model=schemas.Token)
def signup(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    # Check if tenant exists
    db_tenant = db.query(models.Tenant).filter(models.Tenant.email == tenant.email).first()
    if db_tenant:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check Multi-Branch Anti-Duplication Rule for initial branch
    duplicate = db.query(models.Branch).filter(
        (models.Branch.branch_name == tenant.initial_branch_name) |
        (models.Branch.business_address == tenant.initial_business_address) |
        ((models.Branch.latitude == tenant.initial_latitude) & (models.Branch.longitude == tenant.initial_longitude))
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="Initial branch already exists (Duplicate name, address, or coordinates)")

    # Consolidated Onboarding: Commit Tenant and Branch simultaneously
    new_tenant = models.Tenant(
        company_name=tenant.company_name,
        email=tenant.email,
        password=tenant.password, # Plain text as requested
        business_number=tenant.business_number,
        industry_type=tenant.industry_type
    )
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)

    new_branch = models.Branch(
        tenant_id=new_tenant.id,
        branch_name=tenant.initial_branch_name,
        business_address=tenant.initial_business_address,
        latitude=tenant.initial_latitude,
        longitude=tenant.initial_longitude
    )
    db.add(new_branch)
    db.commit()

    logger.info(f"New Tenant Registered: {new_tenant.company_name} with initial branch {new_branch.branch_name}")

    return {
        "access_token": f"mock_secure_token_{new_tenant.id}",
        "token_type": "bearer",
        "tenant_id": new_tenant.id,
        "company_name": new_tenant.company_name
    }

@app.post("/auth/login", response_model=schemas.Token)
def login(login_data: schemas.TenantLogin, db: Session = Depends(get_db)):
    db_tenant = db.query(models.Tenant).filter(
        models.Tenant.email == login_data.email,
        models.Tenant.password == login_data.password
    ).first()

    if not db_tenant:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": f"mock_secure_token_{db_tenant.id}",
        "token_type": "bearer",
        "tenant_id": db_tenant.id,
        "company_name": db_tenant.company_name
    }

# --- BRANCH MANAGEMENT ---

@app.get("/branches", response_model=List[schemas.Branch])
def get_branches(tenant_id: int, db: Session = Depends(get_db)):
    return db.query(models.Branch).filter(models.Branch.tenant_id == tenant_id).all()

@app.post("/branches", response_model=schemas.Branch)
def add_branch(branch: schemas.BranchCreate, tenant_id: int, db: Session = Depends(get_db)):
    # The Multi-Branch Anti-Duplication Rule
    duplicate = db.query(models.Branch).filter(
        (models.Branch.branch_name == branch.branch_name) |
        (models.Branch.business_address == branch.business_address) |
        ((models.Branch.latitude == branch.latitude) & (models.Branch.longitude == branch.longitude))
    ).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="Branch already exists (Duplicate name, address, or coordinates)")

    new_branch = models.Branch(**branch.dict(), tenant_id=tenant_id)
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    return new_branch

@app.delete("/branches/{branch_id}")
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(models.Branch).filter(models.Branch.id == branch_id).first()
    if not db_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    db.delete(db_branch)
    db.commit()
    return {"status": "success", "message": "Branch expunged"}

# --- VOICE ENGINE CORE ---

@app.get("/api/v1/voice/test-sample")
def test_voice_sample():
    # Native Urdu Phonetic Script
    urdu_text = "السلام علیکم! پن پوائنٹ کور کا وائس انجن اب مکمل طور پر فعال ہے۔"

    # Pipeline rendering localized Urdu voice streams natively
    tts = gTTS(text=urdu_text, lang='ur')

    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return StreamingResponse(mp3_fp, media_type="audio/mpeg")

@app.get("/api/v1/agents/health")
def get_agents_health():
    return {
        "interceptor": agent_matrix["interceptor"].catch_mmi_signal(),
        "diagnoser": agent_matrix["diagnoser"].monitor_stack(),
        "escalator": agent_matrix["escalator"].prepare_postgres_migration()
    }

@app.get("/config")
def get_config():
    return {
        "engine_health": "OPTIMAL",
        "security": "LOOSE_SIMULATION",
        "voice_engine": "gTTS_URDU",
        "db_node": "SQLite_LOCAL"
    }
