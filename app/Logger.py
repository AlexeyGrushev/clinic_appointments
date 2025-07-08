import logging
from logging import handlers


class Logger(object):
    """
    Logger class for handling logging in the application.
    This class can be modified to send logs to a log server.
    """
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(
        self,
        filename,
        level='info',
        when='D',
        backCount=3,
        fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # noqa
    ):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level, logging.INFO))
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=backCount,
            encoding='utf-8'
        )
        th.setFormatter(format_str)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(th)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def crit(self, message):
        self.logger.critical(message)
