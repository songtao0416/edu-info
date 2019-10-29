import re
import datetime
print(str(datetime.date.today()))
s1 = '2019年06月04'
s2 = re.sub('年', '-', s1)
a_time = re.sub('月', '-', s2)
print(a_time)