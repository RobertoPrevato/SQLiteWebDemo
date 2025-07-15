@echo off
cd /d "%~dp0"

REM Delete all `.db` files in the db directory
if not exist store (
    mkdir store
)
del /Q store\*.db

REM Delete all migration files inside `migrations/versions/`
del /Q migrations\versions\*.py

REM Run Alembic migration commands
alembic revision --autogenerate -m "structure"
alembic upgrade head

echo Database migration completed successfully!
exit /b 0
