from fastapi import APIRouter, Depends, HTTPException, Response, status
from dependency_injector.wiring import inject, Provide
from inject import Container
from services.storage_proxy import StorageProxy
from constants import Tags


router = APIRouter()


@router.get("/{path:path}", tags = [Tags.STORAGE])
@inject
async def proxy_storage(
  path: str,
  storage_proxy: StorageProxy = Depends(Provide[Container.storage_proxy])
):
  stored_object = storage_proxy.get_stored_object(path)
  if stored_object is None:
    raise HTTPException(detail = "OBJECT_NOT_FOUND", status_code = status.HTTP_404_NOT_FOUND)
  return Response(
    content = stored_object.body,
    media_type = stored_object.content_type
  )
