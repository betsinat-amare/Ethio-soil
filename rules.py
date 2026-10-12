

from schemas import FarmInput


def generate_recommendations(data: FarmInput):
    # 1. Evaluate Soil Acidity (pH)
    acidity_advice = ""
    if data.soil_ph < 5.5:
        acidity_advice = "Soil is strongly acidic. Recommend applying agricultural lime or wood ash."
    else:
        acidity_advice = "Soil pH is within optimal range."

    # 2. Dual-Path Fertilizer Logic
    chemical_prescription = f"Apply {max(0, 100 - data.nitrogen_n)}kg/ha of Urea and {max(0, 50 - data.phosphorus_p)}kg/ha of DAP."
    
    organic_recipe = (
        "Home-Made Organic Recipe: Mix 3 parts decomposed farmyard manure "
        "with 1 part local wood ash to supply organic matter and help buffer soil acidity."
    )

    # 3. Multilingual Dictionary Mock
    messages = {
        "en": {
            "crop": f"Recommended High-Yield Crop for {data.kebele_name}: Wheat / Teff",
            "chemical": chemical_prescription,
            "organic": organic_recipe,
            "acidity": acidity_advice
        },
        "am": {
            "crop": f"ለ{data.kebele_name} የተመረጠ ከፍተኛ ምርት ሰጪ ሰብል፡ ስንዴ / ሰጤ",
            "chemical": f"ኬሚካላዊ ማዳበሪያ: {chemical_prescription}",
            "organic": f"የቤት ውስጥ ኦርጋኒክ ማዳበሪያ ዝግጅት: {organic_recipe}",
            "acidity": f"የአፈር አሲድነት: {acidity_advice}"
        },
        "om": {
            "crop": f"Kuduraan oomisha olaanaa qabuuf filatame {data.kebele_name}: Qamadii",
            "chemical": f"Gabatee Keemikaalaa: {chemical_prescription}",
            "organic": f"Qophii Gabatee Orgaanikii: {organic_recipe}",
            "acidity": f"Sadarkaa Asiidii Biyyee: {acidity_advice}"
        }
    }

    lang = data.language if data.language in messages else "en"
    return messages[lang]