import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    logger.info('Initializing database')
    init_db(db, settings.CREATE_DATASET)
    logger.info('Database initialized')


def main() -> None:
    init()


if __name__ == "__main__":
    main()
