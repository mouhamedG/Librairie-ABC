"""
Module de logging pour la bibliothèque ABC.

Loggue les opérations sensibles et les erreurs
pour l'audit et le debugging.
"""

import logging
import sys
from pathlib import Path
from typing import Any

LOG_FILE_PATH = "logs/librairie_abc.log"
LOGGER_NAME = "librairie_abc"


def setup_logger(
    name: str,
    log_file: str | None = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configure un logger avec un format structuré."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_handler = logging.FileHandler(
                log_path,
                encoding="utf-8",
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except OSError as error:
            logger.warning(
                f"Impossible de créer le fichier "
                f"de log {log_file}: {error}"
            )

    return logger


LOGGER = setup_logger(
    LOGGER_NAME,
    log_file=LOG_FILE_PATH,
    level=logging.INFO,
)


def get_logger() -> logging.Logger:
    """Retourne le logger global."""
    return LOGGER


def format_details(
    details: dict[str, Any] | None = None,
) -> str:
    """Formate les détails optionnels."""
    if details is None:
        return ""

    return f" - {details}"


def log_operation(
    operation: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Loggue une opération métier."""
    logger = get_logger()

    message = (
        "[OPERATION] "
        + operation
        + format_details(details)
    )

    logger.info(message)


def log_error(
    error_type: str,
    error_msg: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Loggue une erreur applicative."""
    logger = get_logger()

    message = (
        "["
        + error_type
        + "] "
        + error_msg
        + format_details(details)
    )

    logger.error(message)


def log_warning(
    warning_msg: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Loggue un avertissement applicatif."""
    logger = get_logger()

    message = (
        "[WARNING] "
        + warning_msg
        + format_details(details)
    )

    logger.warning(message)


def log_validation_error(
    field: str,
    reason: str,
) -> None:
    """Loggue une erreur de validation."""
    log_error(
        "VALIDATION_ERROR",
        f"Validation échouée pour '{field}'",
        {"raison": reason},
    )


def log_security_event(
    event: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Loggue un événement de sécurité."""
    logger = get_logger()

    message = (
        "[SECURITY_EVENT] "
        + event
        + format_details(details)
    )

    logger.warning(message)

    