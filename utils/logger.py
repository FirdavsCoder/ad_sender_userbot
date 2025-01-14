import logging


def setup_logger(name, log_file, level=logging.INFO):
    """
    Logger sozlamalarini o'rnatadi.

    :param name: logger nomi
    :param log_file: loglar yoziladigan fayl
    :param level: log darajasi (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Fayl handerini yaratamiz
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Loggerni sozlaymiz
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)

    return logger