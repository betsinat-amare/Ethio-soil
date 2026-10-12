def generate_farmer_sms(kebele: str, crop: str, chemical: str, organic: str) -> str:
    """
    Formats the recommendation into a concise, action-oriented SMS message in Amharic 
    suitable for basic feature-phone users.
    """
    sms_text = (
        f"ኢትዮ-ሶይል AI (EthioSoil-AI):\n"
        f"ቀበሌ: {kebele}\n"
        f"ተስማሚ ሰብል: {crop}\n"
        f"ማዳበሪያ: {chemical[:50]}...\n"
        f"ኦርጋኒክ: {organic[:50]}..."
    )
    return sms_text