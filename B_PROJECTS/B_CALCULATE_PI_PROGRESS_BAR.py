import sys
from mpmath import mp


def calculate_pi(digits):
    """
    Calculate the value of pi using the mpmath library.
    Returns the value of pi as a string with the specified number of digits.
    """
    mp.dps = digits  # Set the decimal places for mpmath
    pi = mp.pi
    return str(pi)


def write_to_file(filename, content):
    """Write the content to a file."""
    with open(filename, 'w') as file:
        file.write(content)


def update_progress(progress):
    """Update and display the progress bar."""
    bar_length = 50
    filled_length = int(round(bar_length * progress))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: [{bar}] {progress:.1%}')
    sys.stdout.flush()


def main():
    digits = int(input("DIGITS?: "))
    filename = "C:/Users/botoole/Videos/BX STUFF/CODING DOCS/Pi_Digits.txt"

    pi = calculate_pi(digits)
    write_to_file(filename, pi)

    # Update progress bar
    update_progress(1.0)

    print(f"\nCOMPLETE:  FILE_PATH:  {filename}.")


if __name__ == "__main__":
    main()
