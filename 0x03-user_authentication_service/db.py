"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password):
        """To add a new user to the database"""

        new_user = User(email=email, hashed_password=hashed_password)
        self._session
        self.__session.add(new_user)
        self.__session.commit()
        return new_user

    def find_user_by(self, *args, **kwargs):
        """To  get a user using kwargs"""

        from sqlalchemy.orm.exc import NoResultFound
        from sqlalchemy.exc import InvalidRequestError

        self._session
        try:
            user = self.__session.query(User).filter_by(**kwargs).one()
            return user
        except (InvalidRequestError, NoResultFound):
            raise

    def update_user(self, user_id, *args, **kwargs):
        """A method to update a user instance"""

        # list the allowed attributes
        attributes = [
            'id', 'email', 'hashed_password',
            'session_id', 'reset_token'
        ]

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key in attributes:
                setattr(user, key, value)
            else:
                raise ValueError
        self.__session.commit()
        return None
