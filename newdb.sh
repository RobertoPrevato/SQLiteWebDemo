rm store/*.db
rm migrations/versions/*.py
alembic revision --autogenerate -m "structure"
alembic upgrade head
