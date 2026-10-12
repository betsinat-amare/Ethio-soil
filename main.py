from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import FarmInput, RecommendationResponse
from services import rec_service
from models_db import SessionLocal, FarmAdvisoryLog, init_db

app = FastAPI(
    title="EthioSoil-AI Backend API",
    description="Backend service for hyper-localized crop recommendation and dual fertilizer optimization.",
    version="1.0.0"
)

# Enable CORS so frontend dashboards or mobile apps can talk to this API without blocked requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on application startup
@app.on_event("startup")
def startup_event():
    init_db()

# Dependency to get database session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": "EthioSoil-AI",
        "message": "Welcome to the EthioSoil-AI API service."
    }

@app.post("/api/v1/recommend", response_model=RecommendationResponse)
def get_recommendation(payload: FarmInput, db = Depends(get_db)):
    try:
        # Generate full ML & rules recommendation (including SoilGrids GPS lookup if provided)
        result = rec_service.generate_full_advisory(payload)
        
        # Format point geometry string for PostGIS if GPS coordinates are provided
        point_wkt = None
        if payload.latitude and payload.longitude:
            point_wkt = f'POINT({payload.longitude} {payload.latitude})'

        # Persist advisory log to PostgreSQL database
        db_log = FarmAdvisoryLog(
            kebele_name=payload.kebele_name,
            farm_size_hectares=payload.farm_size_hectares,
            geom=point_wkt,
            soil_ph=payload.soil_ph,
            nitrogen_n=payload.nitrogen_n,
            phosphorus_p=payload.phosphorus_p,
            potassium_k=payload.potassium_k,
            rainfall=payload.rainfall,
            recommended_crop=result.get("recommended_crop"),
            acidity_status=result.get("acidity_status")
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)

        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/logs")
def get_all_farm_logs(skip: int = 0, limit: int = 50, db = Depends(get_db)):
    """
    Retrieves all saved farm advisory recommendation logs from the PostgreSQL database.
    """
    try:
        logs = db.query(FarmAdvisoryLog).offset(skip).limit(limit).all()
        
        results = []
        for log in logs:
            results.append({
                "id": log.id,
                "kebele_name": log.kebele_name,
                "farm_size_hectares": log.farm_size_hectares,
                "soil_ph": log.soil_ph,
                "recommended_crop": log.recommended_crop,
                "acidity_status": log.acidity_status,
                "created_at": str(log.created_at)
            })
            
        return {
            "success": True,
            "total_records": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/send-sms")
def get_farmer_sms_advisory(payload: FarmInput):
    """
    Generates a concise Amharic SMS text message tailored for direct farmer delivery 
    on basic mobile phones.
    """
    try:
        # Get standard full recommendation
        result = rec_service.generate_full_advisory(payload)
        
        # Generate Amharic SMS representation
        amharic_sms = rec_service.generate_amharic_sms(payload, result.get("recommended_crop", "Wheat/Teff"))
        
        return {
            "success": True,
            "recipient_language": "am",
            "sms_content": amharic_sms,
            "character_count": len(amharic_sms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))