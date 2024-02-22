from app.database import async_session_maker
import codecs
import csv
from typing import Literal

from fastapi import UploadFile

from app.exceptions import CannotAddDataToDatabase, CannotProcessCSV
from app.importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format


class ImporterService:
    @classmethod
    async def service_import_data_to_table(
            cls,
            file: UploadFile,
            table_name: Literal["hotels", "rooms", "bookings"]
    ):
        ModelDAO = TABLE_MODEL_MAP[table_name]
        csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=";")
        data = convert_csv_to_postgres_format(csvReader)
        file.file.close()

        if not data:
            raise CannotProcessCSV

        async with async_session_maker() as session:
            added_data = await ModelDAO.add_bulk(session, data)
            await session.commit()

        if not added_data:
            raise CannotAddDataToDatabase
