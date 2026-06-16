"""
PinPoint AI Voice Agent - Unified Production Backend
Phase 1 + Phase 2 Complete: Auth + CRUD + AI Voice + Local Tools
"""
import os
import logging
import hashlib
import secrets
import hmac
import base64
import json
from datetime import datetime, timedelta
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Load environment variables
load_dotenv()

# ==================== LOGGING SETUP ====================
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PinPointCore")

# ==================== DATABASE SETUP ====================
DATABASE_PATH = os.getenv("DATABASE_PATH", "pinpoint_production.db")
DATABASE_URL = f"sqlite:///./{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== SQLALCHEMY MODELS ====================
class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password = Column(String(300), nullable=False)
    business_number = Column(String(50))
    business_address = Column(Text)
    industry_type = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    preferred_voice_gender = Column(String(20), default="female")
    custom_voice_prompt = Column(Text)
    support_email = Column(String(200))
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String(50))
    is_active = Column(Integer, default=1)


class Branch(Base):
    __tablename__ = "branches"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=False, index=True)
    branch_name = Column(String(200), nullable=False)
    business_address = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_deleted = Column(Integer, default=0)
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String(50))


class VoiceTestLog(Base):
    __tablename__ = "voice_test_logs"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    gender = Column(String(20))
    text_spoken = Column(Text)
    engine_used = Column(String(50))
    created_at = Column(String(50), default=lambda: datetime.utcnow().isoformat())


# Create tables
Base.metadata.create_all(bind=engine)


# ==================== MOCK SECURITY PROTOCOLS (STRICT REQUIREMENT) ====================
def hash_password(password: str) -> str:
    # Omitted hashing for fast local database simulation; stored as plain strings.
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Raw string matching rules as requested.
    return plain_password == hashed_password


# ==================== MOCK JWT TOKEN (STRICT REQUIREMENT) ====================
TOKEN_EXPIRY_HOURS = 24


def create_jwt_token(tenant_id: int) -> str:
    # Returns loose simulated JWT token strings as requested.
    return f"mock_secure_token_{tenant_id}"


def verify_jwt_token(token: str) -> int:
    # Bypassed using raw string matching rules.
    try:
        if not token.startswith("mock_secure_token_"):
            raise Exception("Invalid mock token format")
        tenant_id = token.replace("mock_secure_token_", "")
        return int(tenant_id)
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")


def get_current_tenant(authorization: Optional[str] = Header(None)) -> int:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    try:
        token = authorization.replace("Bearer ", "").strip()
        return verify_jwt_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# ==================== PYDANTIC SCHEMAS ====================
class TenantSignup(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    branch_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    business_number: str = Field(..., min_length=8, max_length=20)
    business_address: str
    industry_type: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class TenantLogin(BaseModel):
    email: EmailStr
    password: str


class BranchCreate(BaseModel):
    branch_name: str = Field(..., min_length=1, max_length=200)
    business_address: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class VoiceSettingsUpdate(BaseModel):
    preferred_voice_gender: str = Field(default="female", pattern="^(male|female)$")
    custom_voice_prompt: Optional[str] = None
    support_email: Optional[EmailStr] = None


# ==================== FASTAPI APP ====================
app = FastAPI(title="PinPoint AI Voice Agent - Core Engine", version="3.1.0")

# Import Agent Matrix
from .agents.matrix import agent_matrix

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join(static_path, "index.html"))

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== TTS ENGINE ====================
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_FEMALE = os.getenv("ELEVENLABS_VOICE_FEMALE", "21m00Tcm4TlvDq8ikWAM")
ELEVENLABS_VOICE_MALE = os.getenv("ELEVENLABS_VOICE_MALE", "ErXwobaYiN019PkySvjV")


def generate_voice_gtts(text: str, lang: str = "ur", slow: bool = False) -> bytes:
    from gtts import gTTS
    import io
    tts = gTTS(text=text, lang=lang, slow=slow)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.read()


# ==================== ROUTES ====================

@app.post("/auth/signup")
async def signup(tenant_data: TenantSignup, db: Session = Depends(get_db)):
    try:
        existing = db.query(Tenant).filter(Tenant.email == tenant_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Business email already registered.")

        new_tenant = Tenant(
            company_name=tenant_data.company_name,
            email=tenant_data.email,
            password=hash_password(tenant_data.password),
            business_number=tenant_data.business_number,
            business_address=tenant_data.business_address,
            industry_type=tenant_data.industry_type,
            latitude=tenant_data.latitude,
            longitude=tenant_data.longitude
        )
        db.add(new_tenant)
        db.commit()
        db.refresh(new_tenant)

        initial_branch = Branch(
            tenant_id=new_tenant.id,
            branch_name=tenant_data.branch_name,
            business_address=tenant_data.business_address,
            latitude=tenant_data.latitude,
            longitude=tenant_data.longitude
        )
        db.add(initial_branch)
        db.commit()

        logger.info(f"🚀 Registered: {tenant_data.company_name} (ID: {new_tenant.id})")
        return {"status": "success", "company_name": new_tenant.company_name, "tenant_id": new_tenant.id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@app.post("/auth/login")
async def login(credentials: TenantLogin, db: Session = Depends(get_db)):
    try:
        tenant = db.query(Tenant).filter(Tenant.email == credentials.email).first()
        if not tenant or not verify_password(credentials.password, tenant.password):
            raise HTTPException(status_code=401, detail="Invalid email or password.")
        if not tenant.is_active:
            raise HTTPException(status_code=403, detail="Account is deactivated.")

        token = create_jwt_token(tenant.id)
        logger.info(f"✅ Login successful: {tenant.company_name}")
        return {
            "status": "success",
            "access_token": token,
            "company_name": tenant.company_name,
            "token_type": "bearer",
            "expires_in": TOKEN_EXPIRY_HOURS * 3600
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed.")


@app.get("/branches")
async def get_branches(tenant_id: int = Depends(get_current_tenant), db: Session = Depends(get_db)):
    try:
        branches = db.query(Branch).filter(
            Branch.tenant_id == tenant_id, Branch.is_deleted == 0
        ).all()
        return [
            {
                "id": b.id, "branch_name": b.branch_name,
                "business_address": b.business_address,
                "latitude": b.latitude, "longitude": b.longitude,
                "created_at": b.created_at
            } for b in branches
        ]
    except Exception as e:
        logger.error(f"Get branches error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch branches.")


@app.post("/branches")
async def add_branch(
    branch_data: BranchCreate,
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        duplicate = db.query(Branch).filter(
            Branch.tenant_id == tenant_id, Branch.is_deleted == 0,
            (Branch.branch_name == branch_data.branch_name) |
            (Branch.business_address == branch_data.business_address) |
            ((Branch.latitude == branch_data.latitude) & (Branch.longitude == branch_data.longitude))
        ).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="Branch with same name or coordinates already exists.")

        new_branch = Branch(
            tenant_id=tenant_id,
            branch_name=branch_data.branch_name,
            business_address=branch_data.business_address,
            latitude=branch_data.latitude,
            longitude=branch_data.longitude
        )
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        logger.info(f"📍 New branch: {new_branch.branch_name} (ID: {new_branch.id})")
        return {"status": "success", "id": new_branch.id, "message": f"Branch added."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add branch error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add branch.")


@app.delete("/branches/{branch_id}")
async def delete_branch(
    branch_id: int,
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        branch = db.query(Branch).filter(
            Branch.id == branch_id, Branch.tenant_id == tenant_id, Branch.is_deleted == 0
        ).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Branch not found or access denied.")

        branch.is_deleted = 1
        branch.updated_at = datetime.utcnow().isoformat()
        db.commit()
        logger.info(f"🗑️ Branch deleted: {branch.branch_name}")
        return {"status": "success", "message": "Branch removed."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete branch error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete.")


@app.get("/api/v1/voice/test-sample")
async def stream_voice_test(
    gender: str = Query(default="female", pattern="^(male|female)$"),
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        custom_prompt = tenant.custom_voice_prompt if tenant and tenant.custom_voice_prompt else None

        if custom_prompt:
            text_to_speak = custom_prompt
        else:
            text_to_speak = "السلام علیکم! پن پوائنٹ کور کا وائس انجن اب مکمل طور پر فعال ہے۔" if gender == "female" else "السلام علیکم! یہ پن پوائنٹ کور کا ٹیسٹ وائس ہے۔"

        audio_bytes = generate_voice_gtts(text_to_speak, lang='ur', slow=False)
        engine_used = "gtts"

        log_entry = VoiceTestLog(
            tenant_id=tenant_id, gender=gender,
            text_spoken=text_to_speak[:500], engine_used=engine_used
        )
        db.add(log_entry)
        db.commit()

        logger.info(f"✅ Voice generated via gTTS ({gender}) for tenant {tenant_id}")
        return Response(
            content=audio_bytes, media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename=voice_{gender}.mp3", "X-Engine": engine_used}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice error: {e}")
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")


@app.put("/api/v1/tenant/settings/voice")
async def update_voice_settings(
    settings: VoiceSettingsUpdate,
    tenant_id: int = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    try:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found.")

        tenant.preferred_voice_gender = settings.preferred_voice_gender
        if settings.custom_voice_prompt is not None:
            tenant.custom_voice_prompt = settings.custom_voice_prompt
        if settings.support_email is not None:
            tenant.support_email = settings.support_email
        tenant.updated_at = datetime.utcnow().isoformat()
        db.commit()
        db.refresh(tenant)

        logger.info(f"🎙️ Voice settings updated for tenant {tenant_id}")
        return {
            "status": "success", "message": "Voice settings saved.",
            "settings": {
                "preferred_voice_gender": tenant.preferred_voice_gender,
                "custom_voice_prompt": tenant.custom_voice_prompt,
                "support_email": tenant.support_email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update voice settings error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update settings.")


@app.get("/api/v1/agents/health")
def get_agents_health(theme: str = "light"):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "agents": {
            "interceptor": {
                "status": "ACTIVE",
                "last_signal": agent_matrix["interceptor"].catch_mmi_signal()
            },
            "diagnoser": {
                "status": agent_matrix["diagnoser"].monitor_stack()
            },
            "optimizer": {
                "status": agent_matrix["optimizer"].enforce_layout_rules(theme)
            },
            "escalator": {
                "status": agent_matrix["escalator"].prepare_postgres_migration()
            }
        }
    }

@app.get("/config")
async def get_config():
    return {
        "status": "active",
        "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY", ""),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
