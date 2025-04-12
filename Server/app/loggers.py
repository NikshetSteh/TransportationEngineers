import logging

base_logger = logging.getLogger("base")
base_logger.setLevel(logging.DEBUG)

std_handler = logging.StreamHandler()
std_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s"
)
std_handler.setFormatter(formatter)

base_logger.addHandler(std_handler)
