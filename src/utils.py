import sys

def print_message(message, error=''):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    if not error:
        logger.info(message)
    else:
        logger.error("{} in line {}:\n{}".format(message, exc_tb.tb_lineno, error))