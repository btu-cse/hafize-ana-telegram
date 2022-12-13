import csv
import datetime
from itertools import cycle, islice

class Menu():
    def __init__(self):
      pass
    def read_csv(self):
      z = 0
      status = []
      with open("yemekhane.csv", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
          status.append(row)
          z += 1
      return status, z

    def get_menu(self):
        x = 2 + datetime.datetime.now().day
        y = 1
        newList = []
        date = []
        newList3 = []
        status, z = self.read_csv()
        for _ in range(z - 2):
            y += 1
            date.append(status[y][0])
            row2 = [status[y][2], status[y][3], status[y][4], status[y][5]]
            row2 = "\n".join(row2)
            newList3.append(row2)
        newList, newDate = islice(newList, x - 3, None), islice(date, x - 3, None)
        newList, newDate = cycle(newList), cycle(newDate)
        newList4 = []
        timer2 = 0
        for t in newList3:
            if t == '\n\n\n':
                d = newList3[timer2].replace('\n\n\n', 'Haftasonu Yemek Hizmeti Yoktur')
                newList4.append(d)
                timer2 += 1
            else:
                newList4.append(t)
                timer2 += 1
        return newList4, date

