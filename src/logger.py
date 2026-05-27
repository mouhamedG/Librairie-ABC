"""
Module de logging pour la bibliothèque ABC.
Loggue les opérations sensibles et erreurs pour audit et debugging.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Optional


def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configure un logger avec format structuré.
    
    Args:
        name: Nom du logger
        log_file: Chemin optionnel du fichier de log
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Format structuré
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optionnel)
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Impossible de créer le fichier de log {log_file}: {e}")
    
    return logger


# Logger global
_logger = None


def get_logger() -> logging.Logger:
    """Obtient le logger global."""
    global _logger
    if _logger is None:
        _logger = setup_logger(
            'librairie_abc',
            log_file='logs/librairie_abc.log',
            level=logging.INFO
        )
    return _logger


def log_operation(operation: str, details: dict = None) -> None:
    """
    Loggue une opération (format structuré).
    
    Args:
        operation: Nom de l'opération (ex: 'ajouter_livre', 'reserver_livre')
        details: Détails supplémentaires (dict)
    """
    logger = get_logger()
    details_str = f" - {details}" if details else ""
    logger.info(f"[OPERATION] {operation}{details_str}")


def log_error(error_type: str, error_msg: str, details: dict = None) -> None:
    """
    Loggue une erreur.
    
    Args:
        error_type: Type d'erreur
        error_msg: Message d'erreur
        details: Détails supplémentaires
    """
    logger = get_logger()
    details_str = f" - {details}" if details else ""
    logger.error(f"[{error_type}] {error_msg}{details_str}")


def log_warning(warning_msg: str, details: dict = None) -> None:
    """
    Loggue un avertissement.
    
    Args:
        warning_msg: Message d'avertissement
        details: Détails supplémentaires
    """
    logger = get_logger()
    details_str = f" - {details}" if details else ""
    logger.warning(f"[WARNING] {warning_msg}{details_str}")


def log_validation_error(field: str, reason: str) -> None:
    """
    Loggue une erreur de validation.
    
    Args:
        field: Champ concerné
        reason: Raison du rejet
    """
    log_error('VALIDATION_ERROR', f"Validation échouée pour '{field}'", {'raison': reason})


def log_security_event(event: str, details: dict = None) -> None:
    """
    Loggue un événement de sécurité.
    
    Args:
        event: Description de l'événement
        details: Détails supplémentaires
    """
    logger = get_logger()
    details_str = f" - {details}" if details else ""
    logger.warning(f"[SECURITY_EVENT] {event}{details_str}")
