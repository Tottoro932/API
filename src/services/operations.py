import csv
from datetime import datetime
from io import StringIO

from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.db import get_session
from src.models.operations import Operations
from src.models.schemas.operations.operations_request import OperationRequest
from src.models.schemas.report.report_request import FileRequest


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self):
        operations = (
            self.session
                .query(Operations)
                .order_by(
                Operations.id.desc()
            )
                .all()
        )
        return operations

    def get(self, operation_id: int) -> Operations:
        operation = (
            self.session
                .query(Operations)
                .filter(
                Operations.id == operation_id
            )
                .first()
        )
        return operation

    def add(self, operation_schema: OperationRequest, created_user_id: int) -> Operations:
        datetime_ = datetime.utcnow()
        operation = Operations(
            **operation_schema.dict(),
            created_at=datetime_,
            created_by=created_user_id,
            modifed_at=datetime_,
            modifed_by=created_user_id
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, operation_schema: OperationRequest, modifed_user_id: int) -> Operations:
        operation = self.get(operation_id)
        for field, value in operation_schema:
            setattr(operation, field, value)
        datetime_ = datetime.utcnow()
        setattr(operation, 'modifed_at', datetime_)
        setattr(operation, 'modifed_by', modifed_user_id)
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()

    def download_operations(self, file_schema: FileRequest) -> StringIO:
        operations = (
            self.session
                .query(Operations)
                .filter(
                Operations.tank_id == file_schema.tank_id,
                Operations.product_id == file_schema.product_id,
                Operations.date_start < file_schema.date_start,
                Operations.date_end > file_schema.date_end
            )
                .all()
        )
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["tank_id", "product_id", "date_start", "date_end"])
        writer.writeheader()
        for operation in operations:
            print(operation)
            writer.writerow(
                {
                    'tank_id': operation.tank_id,
                    'product_id': operation.product_id,
                    'date_start': operation.date_start,
                    'date_end': operation.date_end
                }
            )
        output.seek(0)
        return output

    def get_for_tank(self, tank_id: int):
        operations = (
            self.session
                .query(Operations)
                .filter(
                Operations.tank_id == tank_id
            )
                .all()
        )
        return operations
