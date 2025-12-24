import sys
from pathlib import Path

# Adjustment needed to import modules from parent subdirectories
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine

try:
    connection = engine.connect()
    print("Connection established")
    connection.close()
except Exception as e:
    print(f"Connection error: {e}")