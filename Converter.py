from ErrorHandler import ErrorHandler


class Converter:
    def __init__(self, error_handler: ErrorHandler):
        self._error_handler = error_handler
        self._output_lst = []
        self._op_stack = []

    def convert(self, token_list):
        # convert infix token list to post fix
        for token in token_list:
            if token.get_type() == "Number":
                self._output_lst.append(token.get_value())
            elif token.get_type() == "Open_Paren":
                self._op_stack.append(token)
            elif token.get_type() == "Close_Paren":
                while self._op_stack[-1].get_value() != "(":
                    self._output_lst.append(self._op_stack.pop().get_value())
                # remove (
                self._op_stack.pop()
            else:
                while len(self._op_stack) != 0 and token.get_predcedence() <= self._op_stack[-1].get_predcedence() and self._op_stack[-1].get_value() != "(":
                    self._output_lst.append(self._op_stack.pop().get_value())
                self._op_stack.append(token)
        while len(self._op_stack) != 0:
            self._output_lst.append(self._op_stack.pop().get_value())


    def get_rpn(self):
        return self._output_lst