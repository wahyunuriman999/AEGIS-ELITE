# ==========================================
# AEGIS COGNITIVE RUNTIME PLATFORM
# PROPRIETARY AND CONFIDENTIAL
# Copyright (c) 2024-2026 Wahyu Nur Iman. 
# All rights reserved.
# ==========================================

import hashlib

class RiskAssessor:
    """
    AEGIS Risk Engine:
    Predicts the blast radius and potential regressions caused by a code change.
    """
    def __init__(self, diff_payload: str):
        self.diff_payload = diff_payload

    def calculate_blast_radius(self) -> float:
        """Calculates how many modules might break due to this change."""
        # Mock calculation based on payload length and keywords
        if "interface" in self.diff_payload.lower() or "abstract" in self.diff_payload.lower():
            return 0.85 # High blast radius
        return 0.20

    def get_risk_score(self) -> dict:
        radius = self.calculate_blast_radius()
        risk_level = "CRITICAL" if radius > 0.7 else ("MODERATE" if radius > 0.3 else "LOW")
        
        return {
            "blast_radius_percentage": round(radius * 100, 2),
            "risk_level": risk_level,
            "recommendation": "Require manual Architect approval." if risk_level == "CRITICAL" else "Safe to proceed automatically."
        }

if __name__ == "__main__":
    assessor = RiskAssessor("+ public interface IUserService {")
    print(assessor.get_risk_score())
