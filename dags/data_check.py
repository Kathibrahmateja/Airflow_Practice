from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
spark = SparkSession.builder.appName("Expense_calculator").getOrCreate()
data = spark.read.format("csv").options(header='true', inferSchema='true').load("expense_detail.txt")
# total=data.agg(sum("Amount").alias("Total")).collect()[0]["Total"]
# monthly_df = data.withColumn("Month", date_trunc("month", to_date(col("Date"), "yyyy-MM-dd"))).groupBy("Month").agg(sum("Amount").alias("total"))
# total_expense=monthly_df.select("total").filter(col("Month") == date_trunc("month", current_date())).collect()[0]["total"]
# print(f"Total Expense: ₹{total:.2f}")
# print(f"Monthly Expense: ₹{total_expense:.2f}")
import matplotlib.pyplot as plt
data=data.toPandas()
data.plot(kind="bar", x="Category", y="Amount")
plt.show()