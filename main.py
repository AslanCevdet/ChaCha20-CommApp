import tkinter as tk
import serial.tools.list_ports as list_ports
import serial

# Serial connection
ser = None

# Variables to track message display
display_encrypted = False
display_decrypted = False

# Function to send message
def send_message():
    if ser:
        message = input_entry.get("1.0", tk.END).strip() + '\n'
        ser.write(message.encode())

# Function to receive message
def receive_message():
    global display_encrypted, display_decrypted
    if ser:
        message = ser.readline().decode('iso-8859-1')
        if message.startswith("Encrypted Text:"):
            display_encrypted = True
            display_decrypted = False
            return
        elif message.startswith("Decrypted Text:"):
            display_encrypted = False
            display_decrypted = True
            return

        if display_encrypted:
            encrypted_text.config(state=tk.NORMAL)
            encrypted_text.insert(tk.END, message)
            encrypted_text.config(state=tk.DISABLED)
        elif display_decrypted:
            decrypted_text.config(state=tk.NORMAL)
            decrypted_text.insert(tk.END, message)
            decrypted_text.config(state=tk.DISABLED)

# Function to connect to selected COM port
def connect_serial():
    global ser
    selected_com_port = com_port_var.get()
    selected_baud_rate = baud_rate_var.get()
    try:
        ser = serial.Serial(selected_com_port, selected_baud_rate, timeout=1)
        connect_button.config(state=tk.DISABLED)
        disconnect_button.config(state=tk.NORMAL)
        status_label.config(text="Connected to " + selected_com_port, fg="green")
    except serial.SerialException:
        ser = None
        status_label.config(text="Failed to connect to " + selected_com_port, fg="red")

# Function to disconnect from the serial connection
def disconnect_serial():
    global ser
    if ser:
        ser.close()
        ser = None
        connect_button.config(state=tk.NORMAL)
        disconnect_button.config(state=tk.DISABLED)
        status_label.config(text="Disconnected", fg="black")

# Get available COM ports
available_ports = [port.device for port in list_ports.comports()]

# Create the GUI window
window = tk.Tk()
window.title("ChaCha20 Encryption & Decryption")

# Developer Message
developer_message = "Welcome, type the message you want to encrypt to related box and just hit send! The program " \
                    "automatically encrypt according to the ChaCha20 algorithm. It also shows you the decrypted " \
                    "version so you know the truth ;)"
developer_label = tk.Label(window, text=developer_message, anchor="w", justify="left", wraplength=400)
developer_label.pack(padx=10, pady=5, anchor="w")

# Label
label = tk.Label(window, text="Type for encryption")
label.pack(padx=10, pady=10, anchor="w")

# Input Entry
input_entry = tk.Text(window, width=50, height=5)  # Change from Entry to Text, and set height to 5
input_entry.pack(padx=10, pady=5, anchor="w")

# Send Button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(padx=10, pady=5, anchor="w")

# Encrypted Text Label
encrypted_label = tk.Label(window, text="Encrypted Text:")
encrypted_label.pack(padx=10, pady=4, anchor="w")

# Encrypted Text
encrypted_text = tk.Text(window, width=50, height=8)
encrypted_text.pack(padx=10, pady=5, anchor="w")
encrypted_text.config(state="disabled")  # Set the state to disabled

# Decrypted Text Label
decrypted_label = tk.Label(window, text="Decrypted Text:")
decrypted_label.pack(padx=10, pady=4, anchor="w")

# Decrypted Text
decrypted_text = tk.Text(window, width=50, height=8)
decrypted_text.pack(padx=10, pady=5, anchor="w")
decrypted_text.config(state="disabled")  # Set the state to disabled

# COM Port Label and Dropdown
com_port_frame = tk.Frame(window)
com_port_frame.pack(padx=10, pady=10, anchor="w")

com_port_label = tk.Label(com_port_frame, text="COM Port:")
com_port_label.pack(side=tk.LEFT)

com_port_var = tk.StringVar()
com_port_dropdown = tk.OptionMenu(com_port_frame, com_port_var, *available_ports)
com_port_dropdown.pack(side=tk.LEFT, padx=4)

# Baud Rate Dropdown
baud_rate_frame = tk.Frame(window)
baud_rate_frame.pack(padx=10, pady=10, anchor="w")

baud_rate_label = tk.Label(baud_rate_frame, text="Baud Rate:")
baud_rate_label.pack(side=tk.LEFT)

baud_rate_var = tk.IntVar()
baud_rate_var.set(115200)
baud_rate_dropdown = tk.OptionMenu(baud_rate_frame, baud_rate_var, 7200, 9600, 14400, 57600, 115200, 921600)
baud_rate_dropdown.pack(side=tk.LEFT, padx=4)

# Connection Buttons
connect_button = tk.Button(window, text="Connect", command=connect_serial)
connect_button.pack(padx=10, pady=10, side=tk.LEFT)

disconnect_button = tk.Button(window, text="Disconnect", command=disconnect_serial, state=tk.DISABLED)
disconnect_button.pack(padx=5, pady=9, side=tk.LEFT)

# Connection Status Label
status_label = tk.Label(window, text="Disconnected", fg="black")
status_label.pack(padx=10, pady=(13, 5), anchor="w")

# Receive messages periodically
def check_serial():
    receive_message()
    window.after(100, check_serial)

# Start checking for messages
window.after(100, check_serial)

# Start the GUI event loop
window.mainloop()
