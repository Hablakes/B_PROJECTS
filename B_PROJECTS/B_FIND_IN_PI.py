import tkinter as tk

with open('C:/Users/botoole/Videos/BX STUFF/CODING DOCS/Pi_Billion.txt', 'r') as file:
    pi_digits = file.read().replace('\n', '')


def search_pi(event=None):
    search_number = entry.get()

    if not search_number.isdigit():
        position_label.config(text="Not Digit")
        return

    try:
        index = pi_digits.index(search_number)
    except ValueError as e:
        pass

    start_index = max(0, index - 25)
    end_index = min(index + 25 + len(search_number), len(pi_digits))

    highlighted_digits = pi_digits[start_index:end_index]
    highlighted_digits = highlighted_digits.replace(search_number, f"[{search_number}]", 1)

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"3.14...{highlighted_digits}")

    # Highlight the found string
    start_tag = "1.0 + {}c".format(index - start_index + 8)
    end_tag = "1.0 + {}c".format(index - start_index + len(search_number) + 8)
    result_text.tag_add("highlight", start_tag, end_tag)
    result_text.tag_configure("highlight", background="green", foreground="white")

    result_text.config(state=tk.DISABLED)

    position_label.config(text=f"Found at position: {index + 1}")


# Create the GUI window
window = tk.Tk()
window.title("Pi Digit Search")
window.geometry("800x400")  # Doubled the window size

# Create an entry box for number input
entry = tk.Entry(window)
entry.pack()
entry.bind("<Return>", search_pi)  # Bind the Enter key to the search function

# Create a button to initiate the search
search_button = tk.Button(window, text="Search", command=search_pi)
search_button.pack()

# Create a text widget to display the search result
result_text = tk.Text(window, height=10)
result_text.pack()
result_text.config(state=tk.DISABLED)

# Create a label to display the position of the result
position_label = tk.Label(window, text="")
position_label.pack()

window.mainloop()
