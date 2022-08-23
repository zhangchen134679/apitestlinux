import logging
import colorlog


def logger(get_level="DEBUG", sh_level="INFO", fh_level="INFO", fh_file=None):

    """
    通过handler_logging调用日志模块时
    默认为控制台输出,传入fh_file参数
    开启.txt文本    """

    # 设置时间格式
    fmt = logging.Formatter('%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')

    log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'cyan',
        'WARNING': 'green',
        'ERROR': 'red',  # red
        'CRITICAL': 'bold_red',  # bold_red
    }

    # 初始化收集器
    get_logger = logging.getLogger()
    get_logger.setLevel(get_level)
    get_logger.handlers.clear()

    # 初始化控制台处理器
    sh = logging.StreamHandler()
    sh.setLevel(sh_level)
    sh.setFormatter(fmt)
    get_logger.addHandler(sh)

    console_formatter = colorlog.ColoredFormatter(
        fmt='%(log_color) s%(asctime)s.%(msecs)03d - %(filename)s -> line:%(lineno)d -> [%(levelname)s] : %(message)s',
        datefmt='%Y-%m-%d  %H:%M:%S',
        log_colors=log_colors_config
    )
    sh.setFormatter(console_formatter)

    # 初始化文件处理器
    # 插入文件路径则开启文件处理器
    if fh_file:
        fh = logging.FileHandler(fh_file, mode='a', encoding="utf8")
        fh.setLevel(fh_level)
        fh.setFormatter(fmt)
        get_logger.addHandler(fh)

    return get_logger











































# def get_logger(level=get_logger_level):
#     logger = logging.getLogger()
#     logger.setLevel(level)
#     return logger
#
#
# def stream_handler(level=stream_handler_level):
#     logger = get_logger()
#     sh = logging.StreamHandler()
#     logger.handlers.clear()
#     sh.setLevel(level)
#     fmt = get_matter()
#     sh.setFormatter(fmt)
#     return logger.addHandler(sh)
#
#
# def file_handler(file_name, level=file_handler_level, mode="a", encoding="utf-8"):
#     stream = get_logger()
#     fh = logging.FileHandler(file_name, mode, encoding)
#     fh.setLevel(level)
#     fmt = get_matter()
#     fh.setFormatter(fmt)
#     return stream.addHandler(fh)
#
#
# def get_matter():
#     fmt = logging.Formatter('%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')
#     return fmt


# if __name__ == "__main__":
#     stream_handler()
#     file_handler(logs_path())
#     logging.debug("我是DEBUG")
#     logging.info("我是INFO")



#
# def get_logger(
#         name="root",
#         file=None,
#         logger_level="DEBUG",
#         stream_level="INFO",
#         file_level="INFO",
#         fmt='%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s'):
#
#     """获取到收集器"""
#     logger = logging.getLogger(name)
#     # 设置收集器的级别
#     logger.setLevel(logger_level)
#
#     # 输出管理器
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(stream_level)
#     logger.addHandler(stream_handler)
#
#     # 格式
#     fmt = logging.Formatter(fmt)
#     stream_handler.setFormatter(fmt)
#
#     if file:
#         file_handler = logging.FileHandler(file, encoding='utf8')
#         file_handler.setLevel(file_level)
#         logger.addHandler(file_handler)
#         file_handler.setFormatter(fmt)
#     return logger



# if __name__ == "__main__":
#     from middleware.handler import Handler
#     logging = Handler.logger
#     logging.info("hello, world")























# conf_data = read_yaml(os.path.join(config_path(), "config_write.yml"))
# get_logger_level = conf_data["logging"]["level"]["get_logger"]
# stream_handler_level = conf_data["logging"]["level"]["stream_handler"]
# file_handler_level = conf_data["logging"]["level"]["file_handler"]
# file_handler_mode = conf_data["logging"]["mode"]
#
#
# def get_logger(level=get_logger_level):
#     logger = logging.getLogger()
#     logger.setLevel(level)
#     return logger
#
#
# def stream_handler(level=stream_handler_level):
#     logger = get_logger()
#     sh = logging.StreamHandler()
#     logger.handlers.clear()
#     sh.setLevel(level)
#     fmt = get_matter()
#     sh.setFormatter(fmt)
#     return logger.addHandler(sh)
#
#
# def file_handler(file_name, level=file_handler_level, mode=file_handler_mode, encoding="utf-8"):
#     stream = get_logger()
#     fh = logging.FileHandler(file_name, mode, encoding)
#     fh.setLevel(level)
#     fmt = get_matter()
#     fh.setFormatter(fmt)
#     return stream.addHandler(fh)
#
#
# def get_matter():
#     fmt = logging.Formatter('%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')
#     return fmt



























# def get_logger(level="DEBUG"):
#     logger = logging.getLogger()
#     logger.setLevel(level)
#     return logger
#
#
# def stream_handler(level="INFO"):
#     stream = get_logger()
#     sh = logging.StreamHandler()
#     stream.handlers.clear()
#     sh.setLevel(level)
#     fmt = get_matter()
#     sh.setFormatter(fmt)
#     stream.addHandler(sh)
#     return stream
#
#
# def file_handler(file_name, level="INFO", mode="a", encoding="utf-8"):
#     logger = get_logger()
#     fh = logging.FileHandler(file_name, mode, encoding)
#     fh.setLevel(level)
#     fmt = get_matter()
#     fh.setFormatter(fmt)
#     logger.addHandler(fh)
#     return logger
#
#
# def get_matter():
#     fmt = logging.Formatter('%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')
#     return fmt



# import logging
#
#
# def get_logger(level="DEBUG"):
#     logger = logging.getLogger()
#     logger.setLevel(level)
#     logger.handlers.clear()
#     return logger
#
#
# def stream_handler(level="DEBUG"):
#     stream = get_logger()
#     sh = logging.StreamHandler()
#     sh.setLevel(level)
#     fmt = get_matter()
#     sh.setFormatter(fmt)
#     return stream.addHandler(sh)
#
#
# def file_handler(file_name, level="INFO", mode="a", encoding="utf-8"):
#     logger = get_logger()
#     fh = logging.FileHandler(file_name, mode, encoding)
#     fh.setLevel(level)
#     fmt = get_matter()
#     fh.setFormatter(fmt)
#     return logger.addHandler(fh)
#
#
# def get_matter():
#     fmt = logging.Formatter('%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')
#     return fmt


# class Logging:
#
#     def __init__(self):
#         self.logger = self.logger()
#         self.fmt = self.matter()
#
#     def logger(self, level="DEBUG"):
#         self.logger = logging.getLogger()
#         self.logger.setLevel(level)
#         self.logger.handlers.clear()
#         return self.logger
#
#     def stream_handler(self, level="DEBUG"):
#         sh = logging.StreamHandler()
#         sh.setLevel(level)
#         sh.setFormatter(self.fmt)
#         return self.logger.addHandler(sh)
#
#     def file_handler(self, path, level="INFO", mode="a", encoding="utf-8"):
#         fh = logging.FileHandler(path, mode, encoding)
#         fh.setLevel(level)
#         fh.setFormatter(self.fmt)
#         return self.logger.addHandler(fh)
#
#     def matter(self):
#         fmt = logging.Formatter(
#             '%(asctime)s -- %(filename)s'' -- line:[%(lineno)d] -- %(levelname)s -- %(message)s')
#         return fmt


