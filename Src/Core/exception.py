
class arguments_exception(Exception):
    def __init__(self, field: str, message: str, stack_trace: str = ""):
        self.__message = message.strip()
        self.__stack_trace = stack_trace.strip()
        self.__field = field.strip()

    def __str__(self):
        return f"""Error: Wrong argument {self.__field}
            {self.__message}
            {self.__stack_trace}
        """
