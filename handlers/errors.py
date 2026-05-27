from aiogram import Router
from aiogram.types import ErrorEvent

from utils.logger import setup_logger

router = Router()
logger = setup_logger(__name__)


@router.errors()
async def global_error_handler(event: ErrorEvent) -> bool:
    logger.error(
        "Unhandled exception for update %s: %s",
        event.update,
        event.exception,
        exc_info=event.exception,
    )
    return True
