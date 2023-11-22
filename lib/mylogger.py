def log(level, print_str):
    print(level + print_str + LOGGER.RESET)


class CheckBit:
    ERROR = 1
    INFO = 1 << 2
    WARN = 1 << 3
    DEBUG = 1 << 4
    VERBOSE = 1 << 5


class LOGGER:
    enabled = 0xFF
    RESET = '\033[0m'
    ERROR = '\033[31m'
    INFO = '\033[32m'
    WARN = '\033[33m'
    DEBUG = '\033[34m'
    VERBOSE = '\033[37m'
    MAP = {
        ERROR: CheckBit.ERROR,
        INFO: CheckBit.INFO,
        WARN: CheckBit.WARN,
        DEBUG: CheckBit.DEBUG,
        VERBOSE: CheckBit.VERBOSE,
    }

    @staticmethod
    def disable(level):
        log(LOGGER.DEBUG, 'test is enabled %d' % (LOGGER.MAP[level] & LOGGER.enabled))
        log(LOGGER.VERBOSE, "origin %d target bit: %d" % (LOGGER.enabled, LOGGER.MAP[level]))
        LOGGER.enabled &= (0xFF ^ LOGGER.MAP[level])
        log(LOGGER.VERBOSE, 'disabled %sCOLOR%s current: %d' % (level, LOGGER.VERBOSE, LOGGER.enabled))
        log(LOGGER.DEBUG, 'test is enabled %d' % (LOGGER.MAP[level] & LOGGER.enabled))

    @staticmethod
    def enable(level):
        LOGGER.enabled |= LOGGER.MAP[level]

    @staticmethod
    def log(level, print_str):
        # print('test: %d' % (LOGGER.MAP[level] & LOGGER.enabled))
        if LOGGER.MAP[level] & LOGGER.enabled == 0:
            return
        log(level, print_str)

    @staticmethod
    def debug(print_str):
        LOGGER.log(LOGGER.DEBUG, print_str)

    @staticmethod
    def error(print_str):
        LOGGER.log(LOGGER.ERROR, print_str)

    @staticmethod
    def warn(print_str):
        LOGGER.log(LOGGER.WARN, print_str)

    @staticmethod
    def verbose(print_str):
        LOGGER.log(LOGGER.VERBOSE, print_str)

    @staticmethod
    def info(print_str):
        LOGGER.log(LOGGER.INFO, print_str)
