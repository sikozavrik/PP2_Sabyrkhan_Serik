from datetime import date, timedelta
a = date.today()
b = a - timedelta(days=1)
c = a + timedelta(days=1)
print("Yesterday:", b)
print("Today:", a)
print("Tomorrow:", c)