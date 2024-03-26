# первоначальный вариант

class Expression:
    def __init__(self, string):
        self.string = string

    def evaluate(self):
        return self._evaluate_expression(self.string)

    def _evaluate_expression(self, start_string: str):
        expression = start_string.replace(" ", "")
        # Создаем стеки для чисел и операторов
        numbers = []
        operators = []
        i = 0

        while i < len(expression):
            if expression[i].isdigit():
                # Если текущий символ - цифра, выделяем число и добавляем его в стек чисел
                num = ""
                while i < len(expression) and (expression[i].isdigit()
                                               or expression[i] == '.'
                                               or expression[i] == ','):  # поддержка записи float через ","
                    num += expression[i]
                    i += 1
                num = num.replace(',', '.')
                numbers.append(float(num))
            elif expression[i] == '(':
                # Если текущий символ - открывающая скобка, рекурсивно вычисляем выражение в скобках
                sub_expression = ""
                count_brackets = 1
                i += 1
                while i < len(expression) and count_brackets > 0:
                    if expression[i] == '(':
                        count_brackets += 1
                    elif expression[i] == ')':
                        count_brackets -= 1
                    if count_brackets > 0:
                        sub_expression += expression[i]
                    i += 1
                numbers.append(self._evaluate_expression(sub_expression))
            elif expression[i] in ['+', '-', '*', '/']:
                # Если текущий символ - оператор, добавляем его в стек операторов
                operators.append(expression[i])
                i += 1
            else:
                i += 1

        # Вычисляем результат используя операторы
        while operators:
            op = operators.pop(0)
            if op == '+':
                numbers.insert(0, numbers.pop(0) + numbers.pop(0))
            elif op == '-':
                numbers.insert(0, numbers.pop(0) - numbers.pop(0))
            elif op == '*':
                numbers.insert(0, numbers.pop(0) * numbers.pop(0))
            elif op == '/':
                numbers.insert(0, numbers.pop(0) / numbers.pop(0))

        return numbers[0]

