from random import randint
from time import sleep
from math import sin


def generate_and_add_coords(terminate_flag, end_button_coords_ui):
    delay = 0.1
    with open("data.csv", "a", buffering=1) as file:
        x = 10
        intercept = 10

        while True:

            if terminate_flag[0]:
                print(" Terminating generate_and_add_coords function")
                break

            elif intercept == 200 and x == 710:
                for i in range(22):
                    x_value = randint(
                        int(end_button_coords_ui[0]), int(end_button_coords_ui[2]))
                    y_value = randint(
                        int(end_button_coords_ui[1]), int(end_button_coords_ui[3]))
                    sleep(delay)
                    file.write(f"{x_value},{y_value}\n")
                # x+=20
                # break

            else:
                sleep(delay)
                y = abs(150*sin(x)) + intercept
                file.write(f"{x},{int(y)}\n")
                x += 20
                file.flush()

                if x >= 1830:
                    x = 10
                    intercept += 190
