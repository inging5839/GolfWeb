from datetime import datetime

print(datetime.now().time().strftime("%H:%M"))

if '14' > '15':
    print('좌측이 커요')
else:
    print('우측이 커요')