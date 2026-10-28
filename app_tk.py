import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = pd.DataFrame({
    "Glucose": [90, 110, 145, 160, 100, 135, 170, 95, 125, 155, 105, 180, 115, 140, 88, 165, 120, 150, 98, 175],
    "BMI": [22, 24, 30, 32, 23, 28, 35, 21, 27, 31, 25, 34, 26, 29, 22, 33, 24, 30, 23, 36],
    "Age": [25, 32, 52, 60, 28, 48, 65, 22, 43, 55, 35, 67, 40, 50, 26, 62, 38, 54, 30, 70],
    "FamilyHistory": ["No", "No", "Yes", "Yes", "No", "Yes", "Yes", "No", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"],
    "Outcome": ["No", "No", "Yes", "Yes", "No", "Yes", "Yes", "No", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes"]
})

RED = "#E50920"
DARK_RED = "#A90016"
GREEN = "#00E676"
DARK_GREEN = "#00A85A"
YELLOW = "#FFD600"
PINK = "#FF4F9A"
BLACK = "#050505"
PANEL = "#101010"
PANEL2 = "#181818"
WHITE = "#FFFFFF"
MUTED = "#B8B8B8"
BORDER = "#353535"

root = tk.Tk()
root.title("Diabetes Risk Prediction Using Bayes")
root.geometry("1250x850")
root.minsize(1050, 760)
root.configure(bg=BLACK)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Risk.Horizontal.TProgressbar",
    troughcolor="#303030",
    background=GREEN,
    bordercolor="#303030",
    lightcolor=GREEN,
    darkcolor=GREEN
)

header = tk.Frame(root, bg=RED, height=58)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="♥  Diabetes Risk Prediction Using Bayes",
    font=("Arial", 18, "bold"),
    fg=WHITE,
    bg=RED
).pack(side="left", padx=25)

main = tk.Frame(root, bg=BLACK)
main.pack(fill="both", expand=True, padx=28, pady=18)

hero = tk.Frame(main, bg=BLACK)
hero.pack(fill="x", pady=(0, 18))

tk.Label(
    hero,
    text="Diabetes ",
    font=("Arial", 30, "bold"),
    fg=WHITE,
    bg=BLACK
).pack(side="left")

tk.Label(
    hero,
    text="Risk Prediction",
    font=("Arial", 30, "bold"),
    fg=RED,
    bg=BLACK
).pack(side="left")

tk.Label(
    hero,
    text="USING BAYESIAN APPROACH",
    font=("Arial", 11),
    fg=WHITE,
    bg=BLACK
).pack(anchor="w", pady=(4, 0))

content = tk.Frame(main, bg=BLACK)
content.pack(fill="both", expand=True)

left = tk.Frame(
    content,
    bg=PANEL,
    highlightbackground=RED,
    highlightthickness=1
)
left.pack(side="left", fill="both", expand=True, padx=(0, 10))

right = tk.Frame(
    content,
    bg=PANEL,
    highlightbackground=GREEN,
    highlightthickness=1
)
right.pack(side="left", fill="both", expand=True, padx=(10, 0))

left_header = tk.Frame(left, bg=RED, height=58)
left_header.pack(fill="x")
left_header.pack_propagate(False)

tk.Label(
    left_header,
    text="♟  Patient Information",
    font=("Arial", 16, "bold"),
    fg=WHITE,
    bg=RED
).pack(side="left", padx=18)

tk.Label(
    left_header,
    text="Enter your details below",
    font=("Arial", 10),
    fg=WHITE,
    bg=RED
).pack(side="right", padx=12)

form = tk.Frame(left, bg=PANEL)
form.pack(fill="both", expand=True, padx=24, pady=12)
form.grid_columnconfigure(1, weight=1)

def make_input(label, unit, row):
    tk.Label(
        form,
        text=label,
        font=("Arial", 12, "bold"),
        fg=WHITE,
        bg=PANEL
    ).grid(row=row, column=0, sticky="w", pady=(12, 2))

    tk.Label(
        form,
        text=unit,
        font=("Arial", 10),
        fg=MUTED,
        bg=PANEL
    ).grid(row=row + 1, column=0, sticky="w", pady=(0, 10))

    entry = tk.Entry(
        form,
        font=("Arial", 13),
        bg=BLACK,
        fg=WHITE,
        insertbackground=GREEN,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground="#444444",
        highlightcolor=GREEN
    )
    entry.grid(
        row=row,
        column=1,
        rowspan=2,
        sticky="ew",
        padx=(15, 0),
        pady=9,
        ipady=9
    )
    return entry

glucose_entry = make_input("Glucose Level", "(mg/dL)", 0)
bmi_entry = make_input("BMI", "(kg/m²)", 2)
age_entry = make_input("Age", "(years)", 4)

tk.Label(
    form,
    text="Family History",
    font=("Arial", 12, "bold"),
    fg=WHITE,
    bg=PANEL
).grid(row=6, column=0, sticky="w", pady=(12, 2))

tk.Label(
    form,
    text="(of Diabetes)",
    font=("Arial", 10),
    fg=MUTED,
    bg=PANEL
).grid(row=7, column=0, sticky="w")

family_var = tk.StringVar(value="No")

family_menu = tk.OptionMenu(form, family_var, "No", "Yes")
family_menu.config(
    font=("Arial", 12),
    bg=BLACK,
    fg=WHITE,
    activebackground=PANEL2,
    activeforeground=GREEN,
    relief="solid",
    bd=1,
    highlightthickness=1,
    highlightbackground=GREEN
)
family_menu["menu"].config(
    bg=BLACK,
    fg=WHITE,
    activebackground=GREEN,
    activeforeground=BLACK
)
family_menu.grid(
    row=6,
    column=1,
    rowspan=2,
    sticky="ew",
    padx=(15, 0),
    pady=9,
    ipady=5
)

result_header = tk.Frame(right, bg=GREEN, height=58)
result_header.pack(fill="x")
result_header.pack_propagate(False)

tk.Label(
    result_header,
    text="▥  Prediction Result",
    font=("Arial", 16, "bold"),
    fg=BLACK,
    bg=GREEN
).pack(side="left", padx=18)

tk.Label(
    result_header,
    text="Model Estimate",
    font=("Arial", 10),
    fg=BLACK,
    bg=GREEN
).pack(side="right", padx=12)

result_area = tk.Frame(right, bg=PANEL)
result_area.pack(fill="both", expand=True, padx=15, pady=12)

chart_frame = tk.Frame(result_area, bg=PANEL)
chart_frame.pack(fill="x")

figure, axis = plt.subplots(figsize=(3.1, 2.45), dpi=100)
figure.patch.set_facecolor(PANEL)
axis.set_facecolor(PANEL)

chart_canvas = FigureCanvasTkAgg(figure, master=chart_frame)
chart_canvas.get_tk_widget().pack(fill="x")

def get_risk_color(risk):
    if risk >= 80:
        return RED
    if risk >= 50:
        return YELLOW
    return GREEN


def draw_chart(risk):
    risk_color = get_risk_color(risk)
    axis.clear()
    axis.pie(
        [risk, 100 - risk],
        startangle=90,
        counterclock=False,
        colors=[risk_color, "#333333"],
        wedgeprops={"width": 0.16, "edgecolor": PANEL}
    )
    axis.text(
        0, 0.08, f"{risk:.1f}%",
        ha="center", va="center",
        fontsize=23, fontweight="bold", color=risk_color
    )
    axis.text(
        0, -0.19, "Risk Probability",
        ha="center", va="center",
        fontsize=10, color=WHITE
    )
    axis.set_title(
        "MODEL ESTIMATE",
        fontsize=11,
        fontweight="bold",
        color=GREEN,
        pad=4
    )
    axis.axis("equal")
    figure.tight_layout(pad=0.5)
    chart_canvas.draw()

draw_chart(0)

status_result = tk.Label(
    result_area,
    text="♥  Awaiting Input",
    font=("Arial", 17, "bold"),
    fg=PINK,
    bg=PANEL2,
    pady=12
)
status_result.pack(fill="x", pady=(3, 8))

description = tk.Label(
    result_area,
    text="Enter patient details and click Predict Risk.",
    font=("Arial", 10),
    fg=WHITE,
    bg=PANEL2,
    wraplength=380,
    pady=8
)
description.pack(fill="x")

progress = ttk.Progressbar(
    result_area,
    style="Risk.Horizontal.TProgressbar",
    orient="horizontal",
    mode="determinate",
    maximum=100,
    value=0
)
progress.pack(fill="x", pady=12)

def predict():
    try:
        glucose = float(glucose_entry.get())
        bmi = float(bmi_entry.get())
        age = int(age_entry.get())

        if not np.isfinite([glucose, bmi, age]).all():
            raise ValueError

        if glucose <= 0 or bmi <= 0 or age <= 0:
            raise ValueError

        if glucose > 600 or bmi > 100 or age > 120:
            raise ValueError

        values = [
            "High" if glucose >= 126 else "Normal",
            "High" if bmi >= 25 else "Normal",
            "Older" if age >= 45 else "Young",
            family_var.get()
        ]

        model_data = data.copy()
        model_data["GlucoseGroup"] = np.where(
            model_data["Glucose"] >= 126, "High", "Normal"
        )
        model_data["BMIGroup"] = np.where(
            model_data["BMI"] >= 25, "High", "Normal"
        )
        model_data["AgeGroup"] = np.where(
            model_data["Age"] >= 45, "Older", "Young"
        )

        features = [
            "GlucoseGroup", "BMIGroup", "AgeGroup", "FamilyHistory"
        ]

        probabilities = {}

        for outcome in ["No", "Yes"]:
            class_rows = model_data[model_data["Outcome"] == outcome]
            class_count = len(class_rows)
            probability = class_count / len(model_data)

            for feature, value in zip(features, values):
                count = (class_rows[feature] == value).sum()
                probability *= (count + 1) / (class_count + 2)

            probabilities[outcome] = probability

        total = sum(probabilities.values())
        risk = probabilities["Yes"] / total * 100

        draw_chart(risk)
        progress["value"] = risk

        risk_color = get_risk_color(risk)
        if risk >= 80:
            status_result.config(text="▲  High Risk", fg=RED)
            description.config(text="The model estimates a high diabetes risk. Please consult a healthcare professional.")
        elif risk >= 50:
            status_result.config(text="●  Moderate Risk", fg=YELLOW)
            description.config(text="The model estimates a moderate diabetes risk. Consider lifestyle changes and medical advice.")
        else:
            status_result.config(text="♥  Low Risk", fg=GREEN)
            description.config(text="The model estimates a lower diabetes risk. Maintain healthy habits and regular checkups.")

        style.configure(
            "Risk.Horizontal.TProgressbar",
            background=risk_color,
            lightcolor=risk_color,
            darkcolor=risk_color
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid positive numbers for glucose, BMI and age."
        )

button = tk.Button(
    left,
    text="⌕   PREDICT RISK",
    command=predict,
    font=("Arial", 15, "bold"),
    bg=RED,
    fg=WHITE,
    activebackground=DARK_RED,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    pady=13
)
button.pack(fill="x", padx=55, pady=(5, 25))

tk.Label(
    root,
    text="Educational demonstration only  •  Not a medical diagnosis",
    font=("Arial", 9),
    fg=MUTED,
    bg=BLACK
).pack(pady=(0, 10))

root.mainloop()