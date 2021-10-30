import csv
def clean_csv(CSVNAME):
    unique_restaurant = []
    with open(CSVNAME, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row in unique_restaurant:
                pass
            else:
                unique_restaurant.append(row)

    header = ["Restaurant","Type","Address","Phone","Website"]
    with open(CSVNAME, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerow(header)
        mywriter.writerows(unique_restaurant)