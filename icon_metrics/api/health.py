from fastapi import Depends

from icon_metrics.api.db import get_session


def is_database_online(session: bool = Depends(get_session)):
    return session
