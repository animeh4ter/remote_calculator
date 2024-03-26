from typing import List, Tuple


class Expression:
    """
    Класс для вычисления математических выражений.

    Принимает строковое математическое выражение и вычисляет его результат.
    """

    def __init__(self, string: str):
        """
        Инициализация объекта класса.

        :param string: Строковое математическое выражение.
        """
        self.string = string

    def evaluate(self) -> float:
        """
        Вычисляет результат математического выражения.

        :return: Результат вычисления выражения.
        """

        result = self._evaluate_expression(self.string)
        # Если результат содержит десятичную часть, равную нулю, преобразуем его в целое число
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return result

    @staticmethod
    def _evaluate_expression(start_string: str) -> float:
        """
        Вычисляет результат математического выражения.

        :param start_string: Строковое математическое выражение.
        :return: Результат вычисления выражения.
        """
        expression = start_string.replace(" ", "")
        numbers, operators = Expression._parse_expression(expression)

        # Сначала вычисляем операции умножения и деления
        i = 0
        while i < len(operators):
            if operators[i] in ['*', '/']:
                if operators[i] == '*':
                    numbers[i] *= numbers[i + 1]
                elif operators[i] == '/':
                    if numbers[i + 1] == 0:
                        raise ValueError("Деление на ноль")
                    numbers[i] /= numbers[i + 1]
                numbers.pop(i + 1)
                operators.pop(i)
            else:
                i += 1

        # Теперь вычисляем операции сложения и вычитания
        result = numbers[0]
        for i in range(len(operators)):
            if operators[i] == '+':
                result += numbers[i + 1]
            elif operators[i] == '-':
                result -= numbers[i + 1]

        return result

    @staticmethod
    def _parse_expression(expression: str) -> Tuple[List[float], List[str]]:
        """
        Разбирает строковое математическое выражение на числа и операторы.

        :param expression: Строковое математическое выражение.
        :return: Кортеж из списка чисел и списка операторов.
        """
        numbers = []
        operators = []
        i = 0

        while i < len(expression):
            if expression[i].isdigit():
                num, i = Expression._extract_number(expression, i)
                numbers.append(float(num))
            elif expression[i] == '(':
                sub_expression, i = Expression._extract_sub_expression(expression, i)
                numbers.append(Expression._evaluate_expression(sub_expression))
            elif expression[i] in ['+', '-', '*', '/']:
                operators.append(expression[i])
                i += 1
            else:
                i += 1

        return numbers, operators

    @staticmethod
    def _extract_number(expression: str, i: int) -> Tuple[str, int]:
        """
        Извлекает число из строки выражения.

        :param expression: Строковое математическое выражение.
        :param i: Индекс в строке выражения.
        :return: Число и новый индекс.
        """
        num = ""
        while i < len(expression) and (expression[i].isdigit() or expression[i] in ['.', ',']):
            num += expression[i]
            i += 1
        num = num.replace(',', '.')
        return num, i

    @staticmethod
    def _extract_sub_expression(expression: str, i: int) -> Tuple[str, int]:
        """
        Извлекает подвыражение из строки выражения.

        :param expression: Строковое математическое выражение.
        :param i: Индекс в строке выражения.
        :return: Подвыражение и новый индекс.
        """
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
        return sub_expression, i

# TODO сделать корни, логарифмы и т.п. как в калькуляторе?
