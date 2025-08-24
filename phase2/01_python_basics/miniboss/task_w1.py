'''Develop a Python script that:
Processes a CSV file with sales data (product, price, quantity, date, etc.).
Generates a custom JSON report with aggregated statistics.
Uses advanced functions (lambda, map, filter, reduce).
Employs generators and advanced comprehensions.
Implements robust exception handling for malformed files, corrupt data, or nonexistent paths.'''

import re
import csv
import json
from functools import reduce
class WrongTimeFormat(Exception):
    pass
try:
    with open('phase2/01_python_basics/miniboss/sales.csv', newline='') as f:
        reader = csv.DictReader(f)
        products = []
        for row in reader:
            if re.match(r"\d{4}-\d{2}-\d{2}",row["date"]): #checks if row['date'] follows the indicated format.
                products.append(row)
            else:
                raise WrongTimeFormat("Error, one or more dates in incorrect format (yyyy-mm-dddd)")

    '''Calculate statistics such as:
    Total sales by category.
    Best-selling product.
    Total revenue per day.'''

    def operator(item_category, category, variable):
        for item in item_category:
            filtered_dict = list((filter(lambda x: x[category] == item, products)))
            yield reduce(lambda x, y: x + y, [float(i[variable]) for i in filtered_dict])
    '''the operator function sums prices or total sales(variable) of each item within the 
    category requested(item_category)'''

    def billing():
        for day in days:
            filtered_dict = list((filter(lambda x: x["date"] == day, products)))
            day_billing = reduce(lambda x, y: x + y, [(float(i["price"])*int(i["quantity"])) for i in filtered_dict])
            yield day_billing

    #general summary:
    total_sales = sum([int(i["quantity"]) for i in products])
    total_revenue = sum([float(i["price"]) for i in products])
    print(total_revenue)

    #sales by category:
    categories = {i["category"] for i in products}
    gen = operator(categories, "category", "quantity")
    sales_by_category = [{"category": category, "units sold": next(gen)} for category in categories]
    print(sales_by_category)
    #best-selling product:
    items = {i["product"] for i in products}
    gen = operator(items, "product", "quantity")
    product_ranking = sorted([[item, next(gen)] for item in items], key = lambda x: x[1], reverse = True)
    best_selling_product = {"product": product_ranking[0][0], "units sold": product_ranking[0][1]}
    print(best_selling_product)
    #revenue per day:
    days = sorted({i["date"] for i in products})

    gen = billing() #this is necessary
    daily_billing = [{"date": day, "billing": next(gen)} for day in days] 
    for i in daily_billing:
        print(f"{i["date"]} -- {i["billing"]}")
    #if you put next(billing()) instead of next(gen), a new generator would be created and only the first value would be given

    json_structure = {"total sales": total_sales, 
            "total revenue": total_revenue,
            "sales by category": sales_by_category, 
            "best selling product": best_selling_product,
            "daily billing": daily_billing
            }

    with open("phase2/01_pyhton_basics/miniboss/sales_report.json", "w", encoding="utf-8") as f:
        json.dump(json_structure, f, indent=4, ensure_ascii=False)

except KeyError:
    print("Error. The CSV file format is not correct. " \
    "Check that the file headers are correctly written. " \
    "They should be: date,product,category,price,quantity -- in that order.")

except (TypeError, ValueError):
    print("Error. The CSV file seems to have a problem.")

except FileNotFoundError:
    print("Error. The file 'sales.csv' is not found in the expected location.")
finally:
    print("script finished.")