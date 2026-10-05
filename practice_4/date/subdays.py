from datetime import date, timedelta
a = date.today()
b = a - timedelta(days=5)
print("Today:", a)
print("5 days ago:", b)