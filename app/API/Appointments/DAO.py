from app.Core.Singleton import Singleton
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
