import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Function to load existing data or initialize new data storage
def load_data():
    try:
        return pd.read_csv("bmi_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Weight", "Height", "BMI", "Category"])

# Function to save data to CSV file
def save_data(data):
    data.to_csv("bmi_data.csv", index=False)

# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / (height ** 2)

# Function to categorize BMI into categories
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    elif bmi < 34.9:
        return "Obesity"
    elif bmi < 39.9:
        return "Severely obese"
    else:
        return "Morbidly obese"

# Function to update the BMI display with calculation and category
# Function to update the BMI display with calculation and category
def update_bmi_display(name, weight, height):
    """
    Update the BMI display with calculated BMI and its category after validating the inputs.
    """
    try:
        # Strip any extra spaces
        weight = weight.strip()
        height = height.strip()
        
        # Replace commas with periods (common input mistake)
        weight = weight.replace(",", ".")
        height = height.replace(",", ".")

        # Try converting weight and height to float
        weight = float(weight)
        height = float(height)

        # Ensure height and weight are greater than zero to avoid division by zero
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be greater than zero")

        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)
        
        # Update the display
        bmi_display.config(text=f"{name}, your BMI is {bmi:.2f} ({category})")

        # Check if all necessary data is available before appending
        if name and not pd.isna(weight) and not pd.isna(height) and not pd.isna(bmi) and category:
            # Add data to the DataFrame
            new_row = pd.DataFrame({"Name": [name], "Weight": [weight], "Height": [height], "BMI": [bmi], "Category": [category]})
            global data
            data = pd.concat([data, new_row], ignore_index=True)
            save_data(data)
        else:
            raise ValueError("Incomplete data provided.")

    except ValueError as ve:
        # Show an error message if input is invalid
        if "could not convert" in str(ve):
            messagebox.showerror("Invalid input", "Please enter valid numbers for weight and height (e.g., 70 for weight and 1.75 for height).")
        else:
            messagebox.showerror("Invalid input", str(ve))

def show_history():
    history_window = tk.Toplevel(window)
    history_window.title("BMI History")
    history_text = tk.Text(history_window)
    history_text.pack()

    history_text.insert(tk.END, data.to_string(index=False))

# Function to show BMI trend analysis graph
def show_trend():
    if len(data) > 0:
        plt.figure(figsize=(10, 5))
        for name in data["Name"].unique():
            user_data = data[data["Name"] == name]
            plt.plot(user_data["BMI"], marker='o', label=name)
        plt.title("BMI Trend Analysis")
        plt.xlabel("Record Number")
        plt.ylabel("BMI")
        plt.legend()
        plt.show()
    else:
        messagebox.showinfo("No Data", "No data available for trend analysis.")

# Initialize main window
window = tk.Tk()
window.title("BMI Calculator")

# Load data from CSV or initialize new data storage
data = load_data()

# UI Components for input and display
tk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(window, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
weight_entry = tk.Entry(window)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(window, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
height_entry = tk.Entry(window)
height_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(window, text="Calculate BMI", command=lambda: update_bmi_display(name_entry.get(), weight_entry.get(), height_entry.get())).grid(row=3, column=0, columnspan=2, pady=10)
bmi_display = tk.Label(window, text="")
bmi_display.grid(row=4, column=0, columnspan=2)

tk.Button(window, text="Show History", command=show_history).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(window, text="Show Trend", command=show_trend).grid(row=6, column=0, columnspan=2, pady=5)

window.mainloop()
