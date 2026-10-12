from models_db import SessionLocal, FarmAdvisoryLog

def fetch_logs():
    db = SessionLocal()
    try:
        logs = db.query(FarmAdvisoryLog).all()
        print(f"\n--- Total Farm Advisory Logs: {len(logs)} ---\n")
        
        for log in logs:
            print(f"ID: {log.id} | Kebele: {log.kebele_name}")
            print(f"  - Farm Size: {log.farm_size_hectares} ha")
            print(f"  - Soil pH: {log.soil_ph}")
            print(f"  - Recommended Crop: {log.recommended_crop}")
            print(f"  - Timestamp: {log.created_at}")
            print("-" * 40)
    except Exception as e:
        print(f"Error fetching logs: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fetch_logs()