import sys, time, logging, asyncio
from typing import Dict, List, Tuple
from abc import abstractmethod
from threading import Thread


class LazyCalledLogger(logging.Logger):
    def do_call_handlers(self, record):
        super().callHandlers(record)

    @abstractmethod
    def callHandlers(self, record):
        pass


class LazyCalledLoggerThread:
    daemon_threads = True

    def __init__(self) -> None:
        self.coroutine_loop = None
        self.coroutine_thread = None

    def coroutine_main(self):
        self.coroutine_loop = loop = asyncio.new_event_loop()
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    def start(self):
        if self.coroutine_thread is not None:
            while not self.coroutine_loop:
                # wait for the loop ready
                time.sleep(0.1)
            return
        self.coroutine_thread = Thread(
            target=self.coroutine_main, name="logger-thread", daemon=self.daemon_threads
        )
        self.coroutine_thread.start()

        while not self.coroutine_loop:
            # wait for the loop ready
            time.sleep(0.1)

    def stop(self):
        if self.coroutine_loop:
            self.coroutine_loop.call_soon_threadsafe(self.coroutine_loop.stop)
            self.coroutine_thread.join()
            self.coroutine_loop = None
            self.coroutine_thread = None

    async def _call(self, logger: LazyCalledLogger, record):
        logger.do_call_handlers(record)

    def call_logger_handler(self, logger: LazyCalledLogger, record):
        self.start()
        asyncio.run_coroutine_threadsafe(
            self._call(logger, record), self.coroutine_loop
        )


class CachingLogger(LazyCalledLogger):
    logger_thread: LazyCalledLoggerThread = LazyCalledLoggerThread()

    def callHandlers(self, record):
        CachingLogger.logger_thread.call_logger_handler(self, record)


class LoggerFactory:
    DEFAULT_LOG_FORMAT: str = "[%(asctime)s]-[%(threadName)s]-[%(name)s:%(lineno)d] %(levelname)-4s: %(message)s"

    DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    _LOG_LVELS: Tuple[str] = ("DEBUG", "INFO", "WARN", "ERROR")

    def __init__(
            self,
            log_level: str = "INFO",
            log_format: str = DEFAULT_LOG_FORMAT,
            date_format: str = DEFAULT_DATE_FORMAT,
    ) -> None:
        self.__cache_loggers: Dict[str, CachingLogger] = {}
        self._log_level = (
            log_level.upper()
            if log_level and log_level.upper() in self._LOG_LVELS
            else "INFO"
        )
        self.log_format = log_format
        self.date_format = date_format

        self._handlers: List[logging.Handler] = []

    @property
    def handlers(self) -> List[logging.Handler]:
        if self._handlers:
            return self._handlers
        _handler = logging.StreamHandler(sys.stdout)
        _formatter_ = logging.Formatter(fmt=self.log_format, datefmt=self.date_format)
        _handler.setFormatter(_formatter_)
        _handler.setLevel(self._log_level)
        self._handlers.append(_handler)
        return self._handlers

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, log_level: str):
        self._log_level = (
            log_level.upper()
            if log_level and log_level.upper() in self._LOG_LVELS
            else "INFO"
        )
        _logger_ = self.get_logger("Logger")
        _logger_.info(f"global logger set to {self._log_level}")
        for h in self._handlers:
            h.setLevel(self._log_level)
        for l in self.__cache_loggers.values():
            l.setLevel(self._log_level)

    def add_handler(self, handler: logging.Handler) -> None:
        if self.__cache_loggers:
            self._handlers.append(handler)
        else:
            self.handlers.append(handler)
        for l in self.__cache_loggers.values():
            l.addHandler(handler)

    def remove_handler(self, handler: logging.Handler) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)
        for l in self.__cache_loggers.values():
            l.removeHandler(handler)

    def set_handler(self, handler: logging.Handler) -> None:
        self._handlers.clear()
        self._handlers.append(handler)
        for l in self.__cache_loggers.values():
            for hdlr in l.handlers:
                l.removeHandler(hdlr)
            l.addHandler(handler)

    def get_logger(self, tag: str = "python-simple-http-server") -> logging.Logger:
        if tag not in self.__cache_loggers:
            self.__cache_loggers[tag] = CachingLogger(tag, self._log_level)
            for handler in self.handlers:
                self.__cache_loggers[tag].addHandler(handler)
        return self.__cache_loggers[tag]


_default_logger_factory: LoggerFactory = LoggerFactory()

_logger_factories: Dict[str, LoggerFactory] = {}


def get_logger_factory(tag: str = "") -> LoggerFactory:
    if not tag:
        return _default_logger_factory
    if tag not in _logger_factories:
        _logger_factories[tag] = LoggerFactory()
    return _logger_factories[tag]


def set_level(level) -> None:
    _default_logger_factory.log_level = level


def add_handler(handler: logging.Handler) -> None:
    _default_logger_factory.add_handler(handler)


def remove_handler(handler: logging.Handler) -> None:
    _default_logger_factory.remove_handler(handler)


def set_handler(handler: logging.Handler) -> None:
    _default_logger_factory.set_handler(handler)


def get_logger(tag: str = "python-simple-http-server") -> logging.Logger:
    return _default_logger_factory.get_logger(tag)
