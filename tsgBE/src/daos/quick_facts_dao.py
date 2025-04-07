from sqlalchemy.orm import Session
from src.schemas import response_schemas
from src.models.entities import State, County, QuickFact

class QuickFactDAO:
    def find_all_by_geoid(self, db: Session, geoid: str):
        results = db.query(QuickFact).filter(QuickFact.fips_code == geoid).all()
        return results 
        