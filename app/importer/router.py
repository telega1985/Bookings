from fastapi import APIRouter, Depends, UploadFile, status

from app.importer.service import ImporterService
from app.users.dependencies import get_current_user
from typing import Literal


router_importer = APIRouter(
    prefix="/import",
    tags=["Импорт данных в БД"]
)


@router_importer.post(
    "/{table_name}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)]
)
async def import_data_to_table(
        file: UploadFile,
        table_name: Literal["hotels", "rooms", "bookings"]
):
    return await ImporterService.service_import_data_to_table(file, table_name)
