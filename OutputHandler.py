from Operators import OpData
from Errors import BaseCalcError


class OutputHandler:
    """
    This is the output class used for all the outputs to the cli
    """

    @staticmethod
    def output_data(final_value: float):
        """
        Output func that will make the output an int value if it has no decimal numbers
        :param final_value:
        :return: None
        """
        # check if the value has decimal point
        if final_value % 1 == 0:
            final_value = int(final_value)
        print(f"The value of the expression is: {final_value}")

    @staticmethod
    def output_op_data():
        print("--------------------------")
        for op_type, op_class in OpData.get_op_classes():
            if op_type == "U-":
                op_type = '-'
            print(f"{op_type} : {op_class.get_description()}")
        print("You can also use ( and )")
        print("--------------------------")

    @staticmethod
    def output_main_instructions():
        print("Welcome to my special calculator, to see all the valid operators please write: op")

    @staticmethod
    def output_error(error: str):
        print(error)
