class BankSystem:
    _money: int

    def __init__(self, start_money: int):
        self._money = start_money

    def _check_parameter_type(self, value: int):
        if type(value) != int:
            raise TypeError("Incorrect type")

    def is_can_get(self):
        return self._money > 0

    @property
    def money(self):
        return self._money

    def can_pay(self, money: int):
        return self._money >= money

    def get_money(self, money: int):
        self._check_parameter_type(money)
        if self._money >= money:
            self._money -= money

        return self._money

    def add_money(self, money: int):
        self._check_parameter_type(money)
        self._money += money

    def set_money(self, money: int):
        self._check_parameter_type(money)
        self._money = money
