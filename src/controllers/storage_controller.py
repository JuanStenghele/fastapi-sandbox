from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from dependency_injector.wiring import inject, Provide
from inject import Container
from services.storage_reverse_proxy import StorageReverseProxy
from constants import Tags


router = APIRouter()


@router.get("/{path:path}", tags = [Tags.STORAGE])
@inject
async def storage_reverse_proxy(
  path: str,
  storage_reverse_proxy: StorageReverseProxy = Depends(Provide[Container.storage_reverse_proxy])
):
  stored_object = storage_reverse_proxy.get_stored_object(path)
  if stored_object is None:
    raise HTTPException(detail = "OBJECT_NOT_FOUND", status_code = status.HTTP_404_NOT_FOUND)
  return StreamingResponse(
    content = stored_object.body,
    media_type = stored_object.content_type
  )
