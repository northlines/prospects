import logging
import json
import os
import time
import sys
import traceback
import inspect
import functools
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from flask import request, g, has_request_context

## Local import(s)
sys.path.append('{}/..'.format(os.path.dirname(__file__)))

from core.config import Config

os.makedirs(Config.LOG_DIR, exist_ok=True)

class LevelFilter(logging.Filter):
    def __init__(self, min_level, max_level):
        self.min_level = min_level
        self.max_level = max_level

    def filter(self, record):
        return self.min_level <= record.levelno <= self.max_level

class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        ts = datetime.fromtimestamp(record.created, timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z")
        path = getattr(record, "path", "")
        if path == "":
            path = record.funcName

        level = record.levelname

        return f"({level:<8}) [{ts}] {record.getMessage()} ({path})"

class CostFormatter(logging.Formatter):
    def format(self, record):
        # Champs standards de LogRecord
        standard_attrs = logging.LogRecord(
            name="", level=0, pathname="", lineno=0,
            msg="", args=(), exc_info=None
        ).__dict__.keys()

        # Extra = tout ce qui n'est pas standard
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in standard_attrs
        }

        module_name = record.module
        function_name = record.funcName
            
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": module_name,
            "function": function_name,
            **extra_fields
        }

        log_json = json.dumps(log_record)
        return log_json
    
class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "event": getattr(record, "event", None),
            "ip": getattr(record, "ip", None),
            "path": getattr(record, "path", None),
            "method": getattr(record, "method", None),
            "status": getattr(record, "status", None),
            "duration_ms": getattr(record, "duration_ms", None),
            "user_id": getattr(record, "user_id", None),
            "country": getattr(record, "country", None),
            "query": getattr(record, "query", None),
            "content_length": getattr(record, "content_length", None),
            "user_agent": getattr(record, "user_agent", None)
        }


        if record.exc_info:
            tb = traceback.extract_tb(record.exc_info[2])

            if tb:
                last = tb[-1]   # dernière frame = origine de l'erreur

                log_record["error_desc"] = f'File "{last.filename}", line {last.lineno}, in {last.name}'
                log_record["error_line"] = f' > {last.line}'

            trace = self.formatException(record.exc_info)

            log_record.update({
                f"z{i}": line
                for i, line in enumerate(trace.split("\n"))
            })

        log_json = json.dumps(log_record)
        return log_json

def create_handler(filename, level, min_level=None, max_level=None):

    handler = TimedRotatingFileHandler(
        f"{Config.LOG_DIR}/{filename}",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )

    handler.setLevel(level)
    
    if level == Config.COST_LEVEL:
        handler.setFormatter(CostFormatter())
    else:
        handler.setFormatter(JsonFormatter())

    handler.addFilter(RequestContextFilter())

    if min_level is not None:
        handler.addFilter(LevelFilter(min_level, max_level))

    return handler

def cost(self, message, *args, **kwargs):
    if self.isEnabledFor(Config.COST_LEVEL):
        self._log(Config.COST_LEVEL, message, args, **kwargs)

def metrics(self, message, *args, **kwargs):
    if self.isEnabledFor(Config.METRICS_LEVEL):
        self._log(Config.METRICS_LEVEL, message, args, **kwargs)

def get_logger():
    logger = logging.getLogger("alpy")
    logging.Logger.cost = cost
    logging.Logger.metrics = metrics
    logging.addLevelName(Config.COST_LEVEL, "COST")
    logging.addLevelName(Config.METRICS_LEVEL, "METRICS")

    if logger.handlers:
        return logger

    logger.setLevel(Config.METRICS_LEVEL)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.COST_LEVEL)
    console_handler.setFormatter(ConsoleFormatter())

    if Config.APP_ENV == 'local' or Config.APP_ENV == 'dev':
        console_handler.addFilter(LevelFilter(Config.COST_LEVEL, logging.CRITICAL))
    else:
        console_handler.addFilter(LevelFilter(logging.DEBUG, logging.DEBUG))

    logger.addHandler(console_handler)

    print(f"LOG FILE : {Config.LOG_DIR}/{Config.SERVICE_NAME}.cost.log")

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.cost.log",
            Config.COST_LEVEL,
            Config.COST_LEVEL,
            Config.COST_LEVEL
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.metrics.log",
            Config.METRICS_LEVEL,
            Config.METRICS_LEVEL,
            Config.METRICS_LEVEL
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.debug.log",
            logging.DEBUG,
            logging.DEBUG,
            logging.DEBUG
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.info.log",
            logging.INFO,
            logging.INFO,
            logging.INFO
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.info.log",
            logging.WARNING,
            logging.WARNING,
            logging.WARNING
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.error.log",
            logging.ERROR,
            logging.ERROR,
            logging.ERROR
        )
    )

    logger.addHandler(
        create_handler(
            f"{Config.SERVICE_NAME}.critical.log",
            logging.CRITICAL,
            logging.CRITICAL,
            logging.CRITICAL
        )
    )

    logger.propagate = False

    return logger

class RequestContextFilter:

    def filter(self, record):
        if has_request_context():
            record.ip = request.headers.get(
                "X-Forwarded-For",
                request.remote_addr
            )
            record.path = request.path
            record.method = request.method
            record.user_agent = request.headers.get("User-Agent")
            record.user_id = getattr(g, "user_id", None)
            record.query = request.query_string.decode()
            record.content_length = request.content_length
            record.endpoint = request.endpoint

        else:
            record.ip = None
            record.path = None
            record.method = None
            record.user_agent = None
            record.user_id = None
            record.query = None
            record.content_length = None
            record.endpoint = None

        return True
    
def init_request_metrics(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):

        duration = (time.time() - g.start_time) * 1000

        get_logger().metrics(
            "http_request",
            extra={
                "event": "http_request",
                "duration_ms": duration,
                "status": response.status_code
            }
        )

        if duration > 500:   # endpoint lent
            get_logger().warning(
                "slow_request",
                extra={
                    "event": "slow_request",
                    "duration_ms": duration,
                    "status": response.status_code
                }
            )

        return response
    
def monitor():
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger()

            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)

                duration = time.perf_counter() - start

                logger.metrics(
                    f"{func.__name__} finished in {duration:.4f}s",
                    extra={
                        "funcname": func.__name__,
                        "duration": duration
                    }
                )

                return result

            except Exception as e:
                duration = time.perf_counter() - start
                logger.critical(
                    f"[Exception] {func.__name__} crashed after {duration:.4f}s ({str(e)})",
                    extra={
                        "funcname": func.__name__,
                        "duration": duration
                    },
                    exc_info=True
                )

                raise

        return wrapper

    return decorator