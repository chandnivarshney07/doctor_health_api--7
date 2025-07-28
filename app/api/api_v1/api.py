from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, users ,lifestyle ,medicines ,pathology ,genetic

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(lifestyle.router, prefix="/lifestyle", tags=["lifestyle"])
api_router.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
api_router.include_router(pathology.router, prefix="/pathology", tags=["pathology"])
api_router.include_router(genetic.router, prefix="/genetic", tags=["genetic"])
