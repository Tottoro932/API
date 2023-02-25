from datetime import datetime
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tanks import Tanks
from src.models.schemas.tanks.tanks_request import TankRequest


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Tanks]:
        tanks = (
            self.session
                .query(Tanks)
                .order_by(
                Tanks.id.desc()
                )
                .all()
        )
        return tanks

    def get(self, tank_id: int) -> Tanks:
        tank = (
            self.session
                .query(Tanks)
                .filter(
                Tanks.id == tank_id
                )
                .first()
        )
        return tank

    def add(self, tank_schema: TankRequest, created_user_id: int) -> Tanks:
        datetime_ = datetime.utcnow()
        tank = Tanks(
            **tank_schema.dict(),
            created_at=datetime_,
            created_by=created_user_id,
            modifed_at=datetime_,
            modifed_by=created_user_id
        )
        self.session.add(tank)
        self.session.commit()
        return tank

    def update(self, tank_id: int, tank_schema: TankRequest, modifed_user_id: int) -> Tanks:
        tank = self.get(tank_id)
        for field, value in tank_schema:
            setattr(tank, field, value)
        datetime_ = datetime.utcnow()
        setattr(tank, 'modifed_at', datetime_)
        setattr(tank, 'modifed_by', modifed_user_id)
        self.session.commit()
        return tank

    def delete(self, tank_id: int):
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()

    def change_capacity(self, tank_id: int, capacity: float) -> Tanks:
        tank = self.get(tank_id)
        setattr(tank, 'current_capacity', capacity)
        self.session.commit()
        return tank
