# README

This project is part of my training process in programming, specifically in Python. 
The script reads a CSV file containing product sales data, computes various sales and revenue metrics, and outputs them in a JSON file.

> **Note**: The input CSV file must have the exact same headers as the one provided (`date,product,category,price,quantity`).

---

## Approach: How I tackled this task

1. I started by writing the script to load the CSV file and convert it into a list of dictionaries.
2. Then, I focused on the calculations (e.g., total sales, sales per product, revenue per day).
3. Once those calculations were working (with the help of `print()` statements and debugging error messages), I refactored the code to create reusable functions to avoid repetition and cleaned up the logic.
4. After the calculations, I handled the JSON export. I structured the output as a general list of dictionaries that includes the sublists of metrics, called `json_structure`.
5. Finally, I tested potential errors by modifying or deleting the CSV file and added `try-except` blocks to handle exceptions. I also created a custom exception (`WrongTimeFormat`) to be raised in case a date is incorrectly formatted.
6. I added a `finally` block to indicate when the script finishes execution.

---

This task was completed as part of my self-training in Python programming.
