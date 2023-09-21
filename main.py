import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import find_peaks

print("What would you like to proceed?")
print("-> Add new file for finding peaks - 1")
print("-> Continue with actual data - 2")

user_choice = input("")
yes_no = "y"
detection_destination = "n"
smoothing_value = 0

if user_choice == "1":
    while True:
        if yes_no == "y":
            print("Enter new name: ")
            new_file_name = input("")
            file = open("files_name.txt", "a")
            file.write("\n")
            file.write(new_file_name)
            file.close()

        elif yes_no != "y":
            break

        print("Add another file name? [y|n]")
        yes_no = input("")

file = open("files_name.txt", "r+")
number_of_lines = len(open("files_name.txt").readlines())

print("Would you like to detect T-WAVES [BETA]? [y|n]")
detect_TWaves = input("")

print("Would you like to use smoothing [BETA]? [y|n]")
use_smooth = input("")

if use_smooth == "y":
    print("Set smoothing value:")
    smoothing_value = input()
    print("Would you like detect QRS complexes on smoothed signal? [y|n]")
    detection_destination = input("")

for x in range(number_of_lines):
    file_data = file.readline()
    file_data = file_data.rstrip("\n")

    ecg = np.load(file_data)
    ecg_sum_values = 0
    ecg_average = 0

    smooth_ecg_values = 0
    smooth_ecg_ave = 0
    smooth_peaks = 0
    smooth_sum = 0

    second_field = np.zeros(3600)
    number_repetitions = 0
    field_limit = 0
    field_position = 0

    end_cycle = 0

    if use_smooth == "y":
        while end_cycle != 1:
            for a in ecg:
                if (number_repetitions >= field_limit and number_repetitions < (field_limit + int(smoothing_value))):
                    smooth_sum += a

                    if number_repetitions == ((field_limit + int(smoothing_value)) - 1):
                        smooth_ecg_ave = (smooth_sum / int(smoothing_value))
                        second_field[field_position] = smooth_ecg_ave

                number_repetitions += 1

            field_position += 1
            smooth_ecg_ave = 0
            smooth_sum = 0
            number_repetitions = 0
            field_limit += 1

            if field_position >= 3600:
                end_cycle = 1

    if detection_destination == "y":
        for x in second_field:
            ecg_sum_values += x
        ecg_average = (ecg_sum_values / len(ecg))

        peaks, _ = find_peaks(ecg, height=ecg_average, threshold=None, distance=162, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)

        plt.plot(ecg)
        plt.plot(second_field)
        plt.plot(peaks, second_field[peaks], "x")

        if detect_TWaves == "y":
            t_waves, _ = find_peaks(second_field, threshold=None, distance=None, prominence=None, width=27.8, wlen=None, rel_height=0.5, plateau_size=None)
            plt.plot(t_waves, second_field[t_waves], "o")

    else:
        for y in ecg:
            ecg_sum_values += y
        ecg_average = (ecg_sum_values / len(ecg))

        peaks, _ = find_peaks(ecg, height=ecg_average, threshold=None, distance=215, prominence=0.6, width=0.1, wlen=None, rel_height=0.1, plateau_size=None)

        plt.plot(ecg)
        plt.plot(peaks, ecg[peaks], "x")

        if detect_TWaves == "y":
            t_waves, _ = find_peaks(ecg, threshold=None, distance=None, prominence=None, width=27.8, wlen=None, rel_height=0.5, plateau_size=None)
            plt.plot(t_waves, ecg[t_waves], "o")

        if use_smooth == "y":
            plt.plot(second_field)
            plt.show()

    plt.show()

file.close()