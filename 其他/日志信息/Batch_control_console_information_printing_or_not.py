class f:
    def __init__(self):
        self.verbose = True
    def print(self, *args, **kwargs):
        """
        Batch control console information printing or not
        """
        if self.verbose:
            print(*args, **kwargs)