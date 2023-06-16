import mpmath

# Set the desired number of digits
mpmath.mp.dps = 10000  # Adjust this value to the desired number of digits

# Calculate pi
pi = mpmath.pi

# Save pi to a .txt file
file_path = "C:/Users/botoole/Videos/BX STUFF/CODING DOCS/Pi_Digits.txt"

with open(file_path, "w") as file:
    file.write(str(pi))

print(f"Pi calculated with {mpmath.mp.dps} decimal places and saved to {file_path}")


