import logging


def get_logger(name: str) -> logging.Logger:
    """
    Создает и настраивает логгер с заданным именем.

    :param name: Имя логгера.
    :return: Объект логгера.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования

    handler = logging.StreamHandler()  # Создаем обработчик вывода в консоль
    handler.setLevel(logging.DEBUG)  # Устанавливаем уровень для обработчика

    # Формат логов: время | имя логгера | уровень логирования | сообщение
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)  # Добавляем обработчик к логгеру

    return logger