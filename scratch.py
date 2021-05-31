import os
from pathlib import Path

# from project.app import db
basedir = Path(__file__).resolve().parent
uri = os.getenv("DATABASE_URL")  # or other relevant config var if uri.startswith("postgres://"):
uri = uri.replace("postgres://", "postgresql://", 1)
print(uri)
