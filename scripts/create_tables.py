import sys
from pathlib import Path

# Adjustment needed to import modules from parent subdirectories
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Base, engine
from app.models.stock import StockPrice
from app.models.technical_indicator import TechnicalIndicator

Base.metadata.create_all(engine)
print("All tables created succesfully!")