from datetime import date
a = date(2025, 10, 1)
b = date(2025, 10, 5)
days = (b - a).days
sec = days * 24 * 60 * 60
print("Days:", days)
print("Seconds:", sec)