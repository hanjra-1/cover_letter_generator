
import openai
import tkinter as tk
from tkinter import ttk, messagebox
from docx import Document
import json
import os
from tkinter import Canvas

# Set your OpenAI API key
openai.api_key = 'your chatgpt api . paste here'
# File to store user data
data_file = "user_data.json"

# Load user data if available
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        user_data = json.load(file)
else:
    user_data = {}

# Function to save user data
def save_user_data():
    with open(data_file, "w") as file:
        json.dump(user_data, file)

# Function to generate cover letter using OpenAI API (using gpt-3.5-turbo)
def generate_cover_letter(experience, skills, job_title):
    prompt = f"""
    Generate a professional cover letter based on the following:
    
    Job Title: {job_title}
    Work Experience: {experience}
    Skills: {skills}
    
    The letter should be tailored for a job application and have a professional tone.
    """

    try:
        # Call OpenAI's API to generate the cover letter (using gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo instead of text-davinci-003
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        messagebox.showerror("Error", f"Error generating cover letter: {str(e)}")
        return None

# Function to save cover letter to DOCX
def save_to_docx(cover_letter):
    doc = Document()
    doc.add_paragraph(cover_letter)
    file_name = "cover_letter.docx"
    doc.save(file_name)
    messagebox.showinfo("Success", f"Cover letter saved as {file_name}")

# Function to add new user data (experience, skills)
def add_user_data(experience, skills, job_title):
    user_data[job_title] = {"experience": experience, "skills": skills}
    save_user_data()
    messagebox.showinfo("Success", "Data saved successfully!")

# Function to generate cover letter using selected data
def on_generate_click():
    job_title = job_title_combobox.get()

    if job_title not in user_data:
        messagebox.showwarning("Data Not Found", "Please select a valid job title from the list.")
        return

    experience = user_data[job_title]["experience"]
    skills = user_data[job_title]["skills"]

    cover_letter = generate_cover_letter(experience, skills, job_title)
    if cover_letter:
        save_to_docx(cover_letter)

# Function to open the data input window
def open_input_window():
    input_window = tk.Toplevel(root)
    input_window.title("Add New Experience and Skills")

    # Job Title Entry
    ttk.Label(input_window, text="Job Title").grid(row=0, column=0, sticky="e")
    job_title_entry = ttk.Entry(input_window, width=40)
    job_title_entry.grid(row=0, column=1)

    # Experience Entry
    ttk.Label(input_window, text="Work Experience").grid(row=1, column=0, sticky="e")
    experience_text = tk.Text(input_window, width=40, height=6)
    experience_text.grid(row=1, column=1)

    # Skills Entry
    ttk.Label(input_window, text="Skills").grid(row=2, column=0, sticky="e")
    skills_text = tk.Text(input_window, width=40, height=6)
    skills_text.grid(row=2, column=1)

    def save_new_data():
        experience = experience_text.get("1.0", "end-1c")
        skills = skills_text.get("1.0", "end-1c")
        job_title = job_title_entry.get()

        if not experience or not skills or not job_title:
            messagebox.showwarning("Input Missing", "Please provide all fields.")
            return
        
        add_user_data(experience, skills, job_title)
        input_window.destroy()
        job_title_combobox['values'] = list(user_data.keys())  # Update combo box

    ttk.Button(input_window, text="Save Data", command=save_new_data).grid(row=3, columnspan=2)

# Create main window
root = tk.Tk()
root.title("AI Cover Letter Generator")
root.geometry("600x400")
# Disable resizing (non-resizable window)
root.resizable(False, False)  # This line prevents the window from being resizable
root.grid_columnconfigure(0, weight=1)  # Make sure the column stretches with resizing
root.grid_rowconfigure(0, weight=1)  # Make sure the row stretches with resizing

# Set up Canvas to create a light gray background
canvas = Canvas(root, height=400, width=600)
canvas.grid(row=0, column=0, )  # Stretch the canvas to cover all space

# Light gray background
canvas.create_rectangle(0, 45, 600, 100, fill="white")

# Header Label in Center
header_label = ttk.Label(root, text="AI Cover Letter Generator", font=("Helvetica", 16,"bold"),background='white')
header_label.grid(row=0, column=0, )

# Dropdown to select job title
job_title_label = ttk.Label(root, text="Select Job Title")
job_title_label.grid(row=1, column=0, )
job_title_combobox = ttk.Combobox(root, width=40, values=list(user_data.keys()))
job_title_combobox.grid(row=2, column=0,pady=40)

# Function to create custom rounded buttons with blue background and white text
def custom_button(master, text, command):
    button = tk.Button(master, text=text, command=command, relief="flat", bg="#4A90E2", fg="white", font=("Helvetica", 12, "bold"), bd=0)
    button.grid(pady=10)
    
    # Make the button rounded by setting the corner radius
    button.config(width=30, height=2, activebackground="#357ABD", activeforeground="white", borderwidth=0)
    return button

# Generate Cover Letter Button
custom_button(root, "Generate Cover Letter", on_generate_click)

# Button to open input window for adding new experience and skills
custom_button(root, "Add New Experience", open_input_window)

root.mainloop()
