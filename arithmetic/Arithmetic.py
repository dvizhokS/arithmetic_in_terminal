from time import time
from datetime import datetime
from random import randint
from arithmetic.Model import Model


class Arithmetic:
    min_x = 0
    min_y = 0
    max_x = 10
    max_y = 10

    x = 0
    y = 0
    ans = ""
    status = False
    signs = ["+", "-", "*", "/"]
    sign = ""
    string_example = ""
    write_info_example = False
    is_smarty = True
    num_example = 0
    total_example = 0
    example_to_win = 10

    start_time = 0
    end_time = 0

    start_ex_time = 0
    ex_time = 0
    errors = []
    max_time_example_s = 5

    db = None

    def __init__(self):
        self.start_time = int(time())
        self.db = Model()

    def set_min_x(self, min_x):
        self.min_x = min_x

    def set_min_y(self, min_y):
        self.min_y = min_y

    def set_max_x(self, max_x):
        self.max_x = max_x

    def set_max_y(self, max_y):
        self.max_y = max_y

    def set_example_to_win(self, n):
        self.example_to_win = n

    def set_signs(self, signs):
        self.signs = []
        for c in signs:
            self.signs.append(c)

    def set_max_time_example_s(self, time_s):
        self.max_time_example_s = time_s

    def set_write_info_example(self, is_write):
        self.write_info_example = is_write

    def set_smarty(self, smart):
        self.is_smarty = smart

    def get_random_x(self):
        return randint(self.min_x, self.max_x)

    def get_random_y(self):
        return randint(self.min_y, self.max_y)

    def get_ans(self):
        return self.ans

    def check_example(self, ans):
        self.check_ans(ans)
        if self.write_info_example:
            self.print_example_info()

    def check_ans(self, ans):
        self.total_example += 1
        self.ex_time = round(time() - self.start_ex_time)
        if self.ans == ans:
            self.status = True
            self.num_example += 1
        else:
            self.status = False
            if self.is_smarty:
                self.num_example -= 1
            self.errors.append(self.string_example + str(ans))
        self.db.update_data(status=self.status, times=self.ex_time)

    def print_start_info(self):
        start_date = datetime.fromtimestamp(self.start_time).strftime("%d-%m-%Y %H:%M:%S")
        print("start time: {}".format(start_date))
        print("x from {} to {}".format(self.min_x, self.max_x))
        print("y from {} to {}".format(self.min_y, self.max_y))
        print("Signs: {}".format(" ".join(self.signs)))
        if self.is_smarty:
            print("For SMART!")
        else:
            print("For normal")
        print("Example to win = {}".format(self.example_to_win))
        print("------------------------------------")

    def print_example_info(self):
        if self.status:
            print("good!")
        else:
            print("Error!")
        print("example time = {}".format(self.ex_time))
        print("Example {} from {}".format(self.num_example, self.example_to_win))

    def write_total_ans(self):
        print("=============================")
        self.end_time = int(time())
        total_time = round(self.end_time - self.start_time)
        length_errors = len(self.errors)
        if length_errors > 0:
            print("ERRORS:")
            for ex in self.errors:
                print("\t", ex)
        print("Total time = {} s".format(total_time))
        print("Total examples = ", self.total_example)

    def get_write_ans(self):
        ans = input()
        if ans.isnumeric():
            ans = int(ans)
            return ans
        return False

    def generate_example(self):
        self.x = self.get_random_x()
        self.y = self.get_random_y()
        self.sign = self.signs[randint(0, len(self.signs) - 1)]

        if self.sign == "+":
            self.example_sum()
        elif self.sign == "-":
            self.example_difference()
        elif self.sign == "*":
            self.example_product()
        elif self.sign == "/":
            self.example_fraction()

    def build_example(self):
        self.string_example = "{} {} {} = ".format(self.x, self.sign, self.y)
        return self.string_example

    def get_example_from_db(self):
        example = self.db.get_example_not_solved(self.signs)

        if not example:
            example = self.db.get_slow_example(self.signs)
            if not example:
                return False

        self.x = example['x']
        self.y = example['y']
        self.sign = example['sign']
        self.ans = example['ans']
        return True

    def example_sum(self):
        self.ans = self.x + self.y

    def example_difference(self):
        if self.x < self.y:
            self.x, self.y = self.y, self.x
        self.ans = self.x - self.y

    def example_fraction(self):
        while self.y == 0:
            self.y = self.get_random_y()

        ans = self.x * self.y
        self.ans = self.x
        self.x = ans

    def example_product(self):
        self.ans = self.x * self.y

    def print_example(self):
        self.start_ex_time = int(time())

        if self.num_example % 3 == 0:
            if not self.get_example_from_db():
                self.generate_example()
                self.db.insert_data(x=self.x, y=self.y, sign=self.sign, ans=self.ans)
        else:
            self.generate_example()
            self.db.insert_data(x=self.x, y=self.y, sign=self.sign, ans=self.ans)

        self.build_example()
        print(self.string_example, end="")

    def run(self):
        self.print_start_info()

        while self.example_to_win > self.num_example:
            self.print_example()
            ans = self.get_write_ans()
            self.check_example(ans)

        self.write_total_ans()
