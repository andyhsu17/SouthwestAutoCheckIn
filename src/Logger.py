class Logger:
    """
    Logging class

    The higher the debug level, the more it will print
    """
    def __init__(self, debug_level):
        self.debug = debug_level
    def _log0(self, *x):
        print(x)

    def _log1(self, *x):
        if self.debug >= 1:
            print(x)

    def _log2(self, *x):
        if self.debug >= 2:
            print(x)
