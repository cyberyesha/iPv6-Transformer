""" This script implements an IPv6 shortener algorithm using Tkinter for the graphical user interface.
It allows users to input an IPv6 address and transforms it by removing the longest consecutive zeros.
The transformed IPv6 address is displayed in the GUI along with the original input. """

# Date; Dec 23 2023
# Created by; yesha

import tkinter as tk
from tkinter import messagebox
import ipaddress

def transform_ipv6(ipv6_address):
    # Transform IPv6 address by removing longest consecutive zeros.
    try:
        validate_ipv6(ipv6_address)
        hex_segments = ['%x' % int(segment, 16) for segment in ipv6_address.split(':')]
    except (ipaddress.AddressValueError, ValueError):
        raise ValueError("Invalid IPv6 address format")

    start_longest_zeros, len_longest_zeros = find_longest_zeros(hex_segments)
    if len_longest_zeros > 1:
        end_longest_zeros = start_longest_zeros + len_longest_zeros
        hex_segments[start_longest_zeros:end_longest_zeros] = ['']
        if end_longest_zeros == len(hex_segments):
            hex_segments += ['']
        if start_longest_zeros == 0:
            hex_segments = [''] + hex_segments

    return ':'.join(hex_segments)

def validate_ipv6(ipv6_address):
    # Validate IPv6 address.
    ipaddress.IPv6Address(ipv6_address)

def find_longest_zeros(hex_segments):
    # Find the start index and length of the longest consecutive zeros in a list of hexadecimal segments.
    best_start = -1
    best_length = 0
    current_start = -1
    current_length = 0

    for index, segment in enumerate(hex_segments):
        if segment == '0':
            current_length += 1
            if current_start == -1:
                current_start = index
            if current_length > best_length:
                best_length = current_length
                best_start = current_start
        else:
            current_length = 0
            current_start = -1

    return best_start, best_length

def transform_and_display():
    # Transform the input IPv6 address and display the result.
    original_input = input_entry.get()
    try:
        shortened_output = transform_ipv6(original_input)
        result_label.config(text=f"Original IPv6: {original_input}\nTransformed IPv6: {shortened_output}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()  # Create Tkinter root window
root.title("IPv6 Shortener")  # Set window title
root.geometry("500x350")  # Set window size

input_label = tk.Label(root, text="Enter IPv6 address:")  # Create label for input
input_label.pack(pady=10)  # Pack label into the window

input_entry = tk.Entry(root, width=40)  # Create entry widget for input
input_entry.pack(pady=10)  # Pack entry widget into the window

transform_button = tk.Button(root, text="Shorten", command=transform_and_display)  # Create button for transformation
transform_button.pack(pady=10)  # Pack button into the window

result_label = tk.Label(root, text="")  # Create label for displaying result
result_label.pack(pady=10)  # Pack label into the window

root.mainloop()  # Start Tkinter event loop
