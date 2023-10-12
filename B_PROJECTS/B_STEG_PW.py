import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from stegano import lsb

# Initialize the selected_image_path variable
selected_image_path = None

# Caesar cipher encryption and decryption functions
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                shifted = ord(char) + shift_amount
                if shifted > ord('z'):
                    shifted -= 26
                encrypted_text += chr(shifted)
            else:
                shifted = ord(char) + shift_amount
                if shifted > ord('Z'):
                    shifted -= 26
                encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Function to open a file dialog and select an image
def open_image():
    global selected_image_path
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.photo = photo
        selected_image_path = file_path
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, selected_image_path)

# Function to encode a message into the selected image with a password
def encode_message():
    global selected_image_path
    if selected_image_path is None:
        messagebox.showerror("Error", "Please select an image first.")
        return

    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password.")
        return

    message = message_entry.get()
    if not message:
        messagebox.showerror("Error", "Please enter a message.")
        return

    # Apply Caesar cipher encryption to the password
    password_shift = 3  # You can adjust the shift value
    encrypted_password = caesar_encrypt(password, password_shift)

    # Apply Caesar cipher encryption to the message
    message_shift = 3  # You can adjust the shift value
    encrypted_message = caesar_encrypt(message, message_shift)

    # Embed the encrypted password and message in the image
    encoded_image = lsb.hide(selected_image_path, f"{encrypted_password}\n{encrypted_message}")

    # Save the encoded image to a file
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        encoded_image.save(save_path)
        messagebox.showinfo("Success", "Message encoded and saved successfully.")

# Function to decode the message from the selected image
def decode_message():
    global selected_image_path
    if selected_image_path is None:
        messagebox.showerror("Error", "Please select an image first.")
        return

    entered_password = password_entry.get()
    if not entered_password:
        messagebox.showerror("Error", "Please enter the password.")
        return

    try:
        encrypted_data = lsb.reveal(selected_image_path)

        data = encrypted_data.split('\n', 1)
        if len(data) == 2:
            encrypted_password, encrypted_message = data

            # Apply Caesar cipher decryption to the password
            password_shift = 3  # Must match the shift used for encoding
            decrypted_password = caesar_decrypt(encrypted_password, password_shift)

            if entered_password == decrypted_password:
                # Apply Caesar cipher decryption to the message
                message_shift = 3  # Must match the shift used for encoding
                decrypted_message = caesar_decrypt(encrypted_message, message_shift)

                message_entry.delete(0, tk.END)
                message_entry.insert(0, decrypted_message)
                messagebox.showinfo("Decoded Message", "Message decoded and displayed.")
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "Decoding failed.")
    except Exception as e:
        messagebox.showerror("Error", "Decoding failed.")

# Create the main GUI window
window = tk.Tk()
window.title("Steganography with Password")

# Create and configure widgets
select_image_button = tk.Button(window, text="Select Image", command=open_image)
image_label = tk.Label(window)
image_path_label = tk.Label(window, text="Image Path:")
image_path_entry = tk.Entry(window, width=50)
password_label = tk.Label(window, text="Password:")
password_entry = tk.Entry(window, width=50, show="*")  # Mask the password entry
message_label = tk.Label(window, text="Message:")
message_entry = tk.Entry(window, width=50)
encode_button = tk.Button(window, text="Encode Message", command=encode_message)
decode_button = tk.Button(window, text="Decode Message", command=decode_message)

# Place widgets in the window
select_image_button.pack()
image_label.pack()
image_path_label.pack()
image_path_entry.pack()
password_label.pack()
password_entry.pack()
message_label.pack()
message_entry.pack()
encode_button.pack()
decode_button.pack()

# Start the GUI main loop
window.mainloop()
