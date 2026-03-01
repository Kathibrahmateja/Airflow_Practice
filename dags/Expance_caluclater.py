import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import matplotlib.pyplot as plt

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class ExpenseCalculator:
    def __init__(self):
        self.budget=100000
        self.expenses = []
        while True:
            amount = float(input("Enter an expense amount (or -1 to finish): "))
            if amount == -1:
                break
            category = input("Enter the expense category: ")
            date = input("Enter the expense date (YYYY-MM-DD): ")
            self.expenses.append((amount, category, date))
        self.persist_expenses()
        self.read_expenses()

    def persist_expenses(self):
        file_exists = os.path.exists("expense_detail.txt")
        with open("expense_detail.txt", "a", encoding="utf-8") as file:
            if not file_exists:
                file.write("Amount,Category,Date\n")
            for amount, category, date in self.expenses:
                file.write(f"{amount},{category},{date}\n")

    def read_expenses(self):
        spark = SparkSession.builder.appName("Expense_calculator").getOrCreate()
        self.data = spark.read.format("csv").options(header='true', inferSchema='true').load("expense_detail.txt")

    def monthly_summary(self):   
            data_df = self.data.withColumn("Date", to_date(col("Date"), "yyyy-MM-dd"))
            data_df = data_df.withColumn("Month", date_trunc("month", "Date"))
            monthly_summary = data_df.groupBy("Month").agg(sum("Amount").alias("Total_Expense")).orderBy("Month")
            print("Monthly Expense Summary:")
            monthly_summary.show()
            
            
    def category_summary(self):
        category_summary = self.data.groupBy("Category").agg(sum("Amount").alias("Total_Catagory_Expanse")).orderBy("Total_Catagory_Expanse", ascending=False)
        print("Category-wise Expense Summary:")
        category_summary.show()

    def budget_alerts(self, budget):
        monthly_df = self.data.withColumn("Month", date_trunc("month", to_date(col("Date"), "yyyy-MM-dd"))).groupBy("Month").agg(sum("Amount").alias("total"))
        total_expense=monthly_df.select("total").filter(col("Month") == date_trunc("month", current_date())).collect()[0]["total"]
        if total_expense > budget:
            print(f"Alert: Your total expenses of ₹{total_expense:.2f} have exceeded your budget of ₹{budget:.2f}.")
        elif total_expense > budget-5000:
            print(f"Alert: Your total expenses of ₹{total_expense:.2f} have approching your budget of ₹{budget:.2f}.")
        else:
            print(f"Your total expenses of ₹{total_expense:.2f} are within your budget of ₹{budget:.2f}.")

    def calculate_total_expense(self):
        total_expense = self.data.agg(sum("Amount").alias("Total")).collect()[0]["Total"]
        return total_expense

    def calculate_average_expense(self):
        if len(self.expenses) == 0:
            return 0
        average_expense = self.data.agg(avg("Amount").alias("average_expense")).collect()[0]["average_expense"]
        return average_expense

    def calculate_max_expense(self):
        if len(self.expenses) == 0:
            return 0
        max_expense = self.data.agg(max("Amount").alias("Max")).collect()[0]["Max"]
        return max_expense

    def category_level_chart(self):
        category_summary = self.data.groupBy("Category").agg(sum("Amount").alias("Total_Catagory_Expanse")).orderBy("Total_Catagory_Expanse", ascending=False)
        category_summary_pd = category_summary.toPandas()
        category_summary_pd.plot(kind="bar", x="Category", y="Total_Catagory_Expanse")
        plt.show()
        
    
    def calculate_min_expense(self):
        if len(self.expenses) == 0:
            return 0
        min_expense = self.data.agg(min("Amount").alias("Min")).collect()[0]["Min"]
        return min_expense
        
    def expense_summary(self):
        total = self.data.agg(sum("Amount").alias("Total")).collect()[0]["Total"]
        html = f"""
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Expense Summary</title>
        <style>
            body {{
                font-family: Arial;
                margin: 40px;
                background-color: #f4f4f4;
            }}
            table {{
                border-collapse: collapse;
                width: 70%;
                background: white;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            h2 {{
                color: #333;
            }}
        </style>
        </head>

        <body>

        <h2>Expense Summary</h2>

        <table>
        <tr>
        <th>Category</th>
        <th>Amount</th>
        <th>Date</th>
        </tr>
        """

        for amount, category, date in self.data.select("Amount", "Category", "Date").collect():
            html += f"<tr><td>{category}</td><td>₹{amount:.2f}</td><td>{date}</td></tr>"

        html += f"""
        <tr>
        <th>Total</th>
        <th>₹ {total}</th>
        </tr>
        </table>

        </body>
        </html>
        """

        with open("expense_summary.html", "w", encoding="utf-8") as file:
            file.write(html)
    
if __name__ == "__main__":
    calculator = ExpenseCalculator()
    calculator.monthly_summary()
    calculator.category_summary()
    calculator.expense_summary()
    print(f"\nTotal Expense: ₹{calculator.calculate_total_expense():.2f}")
    print(f"Average Expense: ₹{calculator.calculate_average_expense():.2f}")
    print(f"Max Expense: ₹{calculator.calculate_max_expense():.2f}")
    print(f"Min Expense: ₹{calculator.calculate_min_expense():.2f}")
    calculator.budget_alerts(calculator.budget)
    calculator.category_level_chart()