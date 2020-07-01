import sys
import random
sys.path.append("C:\MyLocustProjects\Demo_LocustProject")

from utilities.csvreader import CSVReader

my_reader=CSVReader("C:\MyLocustProjects\Demo_LocustProject\data\credential_csv_newtour.csv").read_data()

print(my_reader)
# userName=my_reader.pop()['UserName']
# password=my_reader.pop()['Password']
# print(userName,password)

userName=random.choice(my_reader)['UserName']
password=random.choice(my_reader)['Password']
print(userName,password)



