import sys
import time
import csv
import urllib.request
from bs4 import BeautifulSoup
from County_Muni_Lists import *
from Clean_csv import clean_csv
import inquirer
#--------------------------------------#
State_Abbreviation = input("Please Enter the State Abbreviation: ")

countylists = []
for item in raw_Countylists:
    if item.find("Muni") != -1:
        countylists.append(item)
    else:
        pass
# ^ raw_Countylists is from County_Muni_Lists.py. It is defined as the Gobals() for that file.
#It then checks each var to see if the name contains "Muni"
#For this reason new counties should be added with the naming convention "CountyName"_Muni_List = ["muni1", "muni2", "muni3"]

questions = [inquirer.List('Search Area', message="Please Choose a County", choices = countylists)]
City_County = inquirer.prompt(questions)
print (City_County)
# ^ Inquirer is a required library. This provides the user a simple pick and choose method...
#...for search

City_County_Confirm = input("Confirm Name of Search Area: ")
if City_County_Confirm in raw_Countylists:
    print (raw_Countylists[City_County_Confirm])
else:
    print("ERROR")
    sys.exit()
# ^ Gets user to confirm the search area and check to see if that area is defined 
#Again these should be defined as array in County_Muni_Lists.py 

Block_Number = input("Please Enter Block Number (list above is an array): ")
# ^ Block number is getting the user to choose where in the county to begin
#ie: what number municipality in the array

CSVNAME_input = input("Please Name the CSV File: ")
CSVNAME = str(CSVNAME_input)+".csv" 
# ^ Gets user to name or define which csv file to write to 

Start_Time = time.time()
#--------------------------------------#
def get_restaurant_links(Search_Area):
    Page_Number = 0
    Restaurant_Links = []
    a = 1
    print("Loading Pages...")
    while Page_Number <= 230:
        Link = ("https://www.yelp.com/search?find_desc=Restaurants&find_loc="+(Search_Area.replace(" ", ""))+"%2C%20"+State_Abbreviation+"&sortby=rating&start="+str(Page_Number))
        response = urllib.request.urlopen(Link)
        soup = BeautifulSoup(response.read(), "lxml")

        for item in soup.find_all("a", {"class": "css-1f2a2s6"}):
            href = item.get("href")
            Restaurant_Links.append(href)
        print("Page "+str(a)+" Done - "+str(Search_Area))
        a += 1
        Page_Number += 10
    print("Pages Loaded")
    return(Restaurant_Links)
# ^ This function checks 24 pages of results for a given municipality (10 results per page)
#It then appends Restaurant_Links with the link to each results yelp page
#Function returns an array full of links to each restaurant in a given municipality 

def get_restaurant_data(RLinks):
    Full_Data_Array = []
    a = len(RLinks)-1
    b = 0
    while a >= b:
        Link = "https://www.yelp.com"+str(RLinks[b])
        response = urllib.request.urlopen(Link)
        soup = BeautifulSoup(response.read(), "lxml")
        Res_Data = []

        for item in soup.find_all("h1", {"class" : "css-m7s7xv"}):
            Res_Name = item.text
            Res_Data.append(Res_Name)
            print(Res_Name)

        Class_166la90 = []
        for item in soup.find_all("a", {"class" : "css-166la90"}):
            if item == None:
                Typeofres = "N/Aabc"
                Class_166la90.append(Typeofres)
            else:
                Typeofres = (item.text)
                Class_166la90.append(Typeofres)
        if len(Class_166la90) > 0:
            Res_Type = Class_166la90[0]
            Res_Data.append(Res_Type)
        else:
            pass

        for item in soup.find_all("p", {"class" : "css-chtywg"}):
            Res_Address = item.text
            Res_Data.append(Res_Address)
        
        Class_1h1j0y3 = []
        for item in soup.find_all("p", {"class" : "css-1h1j0y3"}):
            class_array = item.text
            Class_1h1j0y3.append(class_array)
        if len(Class_1h1j0y3) < 3:
            pass
        else:
            Res_Phone = Class_1h1j0y3[-2]
            if Class_1h1j0y3[-3] == "Ask a question":
                Res_Website = "Website N/A"
            else:
                Res_Website = Class_1h1j0y3[-3]
            Res_Data.append(Res_Phone)
            Res_Data.append(Res_Website)

        Full_Data_Array.append(Res_Data)
        b += 1
    return(Full_Data_Array)
# ^ This function goes through the array of restaurant links... 
#...and returns the Name, Type, Address, Phone Number, and Website 

def run(Muni_List):
    print (len(Muni_List))
    i = int(Block_Number)
    header = ["Restaurant","Type","Address","Phone","Website"]
    while i <= len(Muni_List)-1:
        with open(CSVNAME, 'a', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerow(header)
            mywriter.writerows(get_restaurant_data(get_restaurant_links(Muni_List[i])))
        clean_csv(CSVNAME)
        i += 1
# ^ This function adds the scraped data to the named csv file

#--------------------------------------#
run(raw_Countylists[City_County_Confirm])
# ^ Running the functions
#--------------------------------------#

print("--- %s seconds ---" % (time.time() - Start_Time))
