import logging.handlers
import time


class GetLogger:
    logger = None

    @classmethod
    def get_logger(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger()
            cls.logger.setLevel(logging.INFO)
            sh = logging.StreamHandler()
            th = logging.handlers.TimedRotatingFileHandler(
                filename="./lipaiapi/log/{}.log".format(time.strftime("%Y-%m-%d")), when="midnight",
                interval=1, backupCount=30, encoding="utf-8")
            # ht = logging.handlers.RotatingFileHandler("./lipaiapi/log/log.log", mode="w")
            fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            fm = logging.Formatter(fmt)
            sh.setFormatter(fm)
            th.setFormatter(fm)
            # ht.setFormatter(fm)
            cls.logger.addHandler(sh)
            cls.logger.addHandler(th)
            # cls.logger.addHandler(ht)
        return cls.logger
