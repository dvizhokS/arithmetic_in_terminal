from arithmetic.Arithmetic import Arithmetic
from config import config


if __name__ == "__main__":
    arithmetic = Arithmetic()
    arithmetic.set_min_x(config["min_x"])
    arithmetic.set_max_x(config["max_x"])
    arithmetic.set_min_y(config["min_y"])
    arithmetic.set_max_y(config["max_y"])
    arithmetic.set_signs(config["signs"])
    arithmetic.set_smarty(config["is_smarty"])
    arithmetic.set_write_info_example(config["info_example"])
    arithmetic.set_example_to_win(config["example_to_win"])

    arithmetic.run()

    input("\n\tPres Enter to exit!")
