from fastapi import APIRouter, Depends
from constants import Tags
from objects.health_check import HealthCheckResponse, DeepHealthCheckResponse
from dal.health_check_dal import HealthCheckDAL
from clients.storage_client import StorageClient
from dependency_injector.wiring import inject, Provide
from inject import Container
from sqlmodel import Session
from controllers.dependencies import get_session


router = APIRouter()


@router.get("/health-check", response_model = HealthCheckResponse, tags = [Tags.HEALTH_CHECK])
def health_check():
  return HealthCheckResponse(
    api = "ok"
  )


@router.get("/health-check/deep", response_model = DeepHealthCheckResponse, tags = [Tags.HEALTH_CHECK])
@inject
def deep_health_check(
  session: Session = Depends(get_session),
  health_check_dal: HealthCheckDAL = Depends(Provide[Container.health_check_dal]),
  s3_client: StorageClient = Depends(Provide[Container.s3_client])
):
  return DeepHealthCheckResponse(
    api = "ok",
    postgres_database = "ok" if health_check_dal.health_check(session) else "error",
    storage = "ok" if s3_client.health_check() else "error"
  )
