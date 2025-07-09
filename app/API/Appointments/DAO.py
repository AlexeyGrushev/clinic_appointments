from sqlalchemy import text

from app.Core.Singleton import Singleton
from app.DataBase.Base import async_session
from app.DataBase.DataBaseHelper import DataBaseHelper
from app.DataBase.models.Appointment import Appointment


class AppointmentDAO(DataBaseHelper, metaclass=Singleton):
    """
    This class represents the Data Access Object of the Appointment model.
    It inherits all methods of the DataBaseHelper class, which contains all
    methods for interacting with the model in the database. You can also add
    here other methods that will apply only to this model if
    is needed.


    This DAO uses the Singleton pattern, which ensures that
    has only one object in the whole code.
    """

    model = Appointment

    # For example: This classmethod only aviable for this Data Access Object
    @staticmethod
    async def ping():
        async with async_session() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar_one()
