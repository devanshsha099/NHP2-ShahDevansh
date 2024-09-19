from truck import *
from csvreader import hubs_ref
from csvreader import packages_ref
from csvreader import package_with_note
from csvreader import all_package_list
from csvreader import package_with_deadline
from csvreader import packages_delivered_list
import pandas as pd
import datetime
from csvreader import get_hash_map

# This is the Dijkstra's path-finding algorithm coded by Devansh Shah (Student ID - 000971474).
# This algorithm was coded in PyCharm Python 3.11. The run-point of the application is this file named main.py.
# After running the application, follow the GUI prompt as a guide through the algorithm

selected_option = input("\x1B[3m""""
Welcome to Shah's C950 Dijkstra algorithm prompt.\n
This algorithm aims to find the shortest possible path visiting all the hubs and delivering all the packages while following the guidelines. 
Type the following number keys to execute the desired results. \x1B[0m
'\033[1m
1 --> To start the Dijkstra algorithm to deliver all the packages through the shortest path. 
2 --> To know each individual package's info and arrival times sorted by the location they belong. 
3 --> To know each individual package's delivery status at a desired time.
4 --> To exit
""""\033[0m")

# Option #1 creates a route & feeds all the packages all at once
# It then distributes packages in either Truck 1 1st trip, Truck 2 1st trip or Truck 1 2nd trip. This way Truck 3 is never utilized
# Some packages are assigned manually to meet the deadlines and/or special instructions whilst others are automated



def option_one():
    truck_one = Truck(16, '#1', 0, hubs_ref.get_node_by_index(0), 8, 0, 0)  # Truck #1 starts at Hub Index 0 & leaves at 08:00:00.
    truck_two = Truck(16, '#2', 0, hubs_ref.get_node_by_index(0), 9, 5, 0)  # Truck #2 starts at Hub Index 0 & leaves at 09:05:00 to make sure that all the packages that arrive at 09:05 are sent in this truck
    truck_three = Truck(16, '#3', 0, hubs_ref.get_node_by_index(0), 0, 0, 0)  # Truck #3 is not used

    truck_two_regular_packages = [3, 18, 28]  # Packages that can only be on the Truck #2 & some packages that have to be loaded after 09:05 AM.
    truck_two_priority_packages = [6, 25, 32, 36, 38]  # Packages that have to be together, packages that won't be at the depot till 09:05 AM. Expand this list as required if more priority packages are to be added.
    truck_one_priority_package = [23]


    # Sorts all packages by zip code & holds them all in all_package_list. Later grouped into packages with deadlines & packages with a note
    for packages in packages_ref.group_packages_by_zip().values():
        for package in packages:
            all_package_list.append(package)
    # package_with_deadline holds all the packages with a deadline & removes them from all_package_list if present there
    for package in packages_ref.get_packages_by_deadline():
        if package in all_package_list:
            package_with_deadline.append(package)
            all_package_list.remove(package)
    # package_with_note holds all the packages with a note & any packages still remaining in the all_package_list & removes them from the initial holders if they are present here
    for package in packages_ref.get_packages_by_note():
        if package in all_package_list:
            package_with_note.append(package)
            all_package_list.remove(package)
        if package in package_with_deadline:
            package_with_note.append(package)
            package_with_deadline.remove(package)
    truck_one.insert_regular_package(13, package_with_deadline)
    truck_one.insert_regular_package(14, package_with_note)
    truck_one.insert_regular_package(15, package_with_deadline)
    truck_one.insert_regular_package(16, package_with_note)
    truck_one.insert_regular_package(19, all_package_list)
    truck_one.insert_regular_package(20, package_with_note)
    truck_one.load_priority_packages() # Load all the packages with 09:00 & 10:30 deadlines
    truck_one.load_regular_packages() # Fill it up with the rest
    truck_one.deliver_route() # First iteration of Truck number 1.
    print('Total packages delivered by Truck #1 in this trip: ' + str(len(packages_delivered_list)))
    print('-----------------------------------------------------------------')

    print('Total packages delivered by Truck #1: ' + str(len(packages_delivered_list)))
    print('-----------------------------------------------------------------')


    for package_numb in truck_two_priority_packages:
        truck_two.insert_priority_package(package_numb, package_with_note)

    for package_numb in truck_two_regular_packages:
        truck_two.insert_regular_package(package_numb, package_with_note)

    truck_two.load_regular_packages()
    truck_two.deliver_route()
    truck_one.load_regular_packages()

    # Truck #1 is now on its second iteration
    # The second iteration starts after the 16th package from the Truck 1 is delivered and the truck returns back to WGU
    # The second iteration starts at 10:28:40 AM which is after the address of the package 9 is declared at 10:20 AM
    # The code below changes the address of package 9 from 195 W Oakland Ave to 410 S State St at the time the iteration starts
    # at 10:28:40 AM. The package will now go to the Third District Juvenile Court instead of the Council Hall

    df = pd.read_csv("packageinfo.csv")
    df.loc[7, '195 W Oakland Ave'] = '410 S State St'
    df.to_csv("packageinfo.csv", index=False)

    truck_one.insert_regular_package(9, package_with_note) # Package 9 is inserted into the truck with the updated address
    truck_one.deliver_route()

    print('All packages delivered.')
    print('\nList of packages delivered today: ' + str(packages_delivered_list))
    print('Truck #1 total mileage: ' + str(truck_one.mileage))
    print('Truck #2 total mileage: ' + str(truck_two.mileage))
    print('Total mileage of all delivery trucks today: ' + str(truck_one.mileage + truck_two.mileage + truck_three.mileage))

def option_two():
    truck_one = Truck(16, '#1', 0, hubs_ref.get_node_by_index(0), 8, 0, 0)  # Truck #1 starts at Hub Index 0 & leaves at 08:00:00.
    truck_two = Truck(16, '#2', 0, hubs_ref.get_node_by_index(0), 9, 5, 0)  # Truck #2 starts at Hub Index 0 & leaves at 09:05:00 to make sure that all the packages that arrive at 09:05 are sent in this truck
    truck_three = Truck(16, '#3', 0, hubs_ref.get_node_by_index(0), 0, 0, 0)  # Truck #3 is not used

    truck_two_regular_packages = [3, 18, 28]  # Packages that can only be on the Truck #2 & some packages that have to be loaded after 09:05 AM.
    truck_two_priority_packages = [6, 25, 32, 36, 38]  # Packages that have to be together, packages that won't be at the depot till 09:05 AM. Expand this list as required if more priority packages are to be added.
    truck_one_priority_package = [23]

    # Sorts all packages by zip code & holds them all in all_package_list. Later grouped into packages with deadlines & packages with a note
    for packages in packages_ref.group_packages_by_zip().values():
        for package in packages:
            all_package_list.append(package)
    # package_with_deadline holds all the packages with a deadline & removes them from all_package_list if present there
    for package in packages_ref.get_packages_by_deadline():
        if package in all_package_list:
            package_with_deadline.append(package)
            all_package_list.remove(package)
    # package_with_note holds all the packages with a note & any packages still remaining in the all_package_list & removes them from the initial holders if they are present here
    for package in packages_ref.get_packages_by_note():
        if package in all_package_list:
            package_with_note.append(package)
            all_package_list.remove(package)
        if package in package_with_deadline:
            package_with_note.append(package)
            package_with_deadline.remove(package)
    truck_one.insert_regular_package(13, package_with_deadline)
    truck_one.insert_regular_package(14, package_with_note)
    truck_one.insert_regular_package(15, package_with_deadline)
    truck_one.insert_regular_package(16, package_with_note)
    truck_one.insert_regular_package(19, all_package_list)
    truck_one.insert_regular_package(20, package_with_note)
    truck_one.load_priority_packages()  # Load all the packages with 09:00 & 10:30 deadlines
    truck_one.load_regular_packages()  # Fill it up with the rest
    truck_one.print_individual_package_info()  # First iteration of Truck number 1.

    for package_numb in truck_two_priority_packages:
        truck_two.insert_priority_package(package_numb, package_with_note)

    for package_numb in truck_two_regular_packages:
        truck_two.insert_regular_package(package_numb, package_with_note)

    truck_two.load_regular_packages()
    truck_two.print_individual_package_info()
    truck_one.load_regular_packages()

    # Truck #1 is now on its second iteration
    # The second iteration starts after the 16th package from the Truck 1 is delivered and the truck returns back to WGU
    # The second iteration starts at 10:28:40 AM which is after the address of the package 9 is declared at 10:20 AM
    # The code below changes the address of package 9 from 195 W Oakland Ave to 410 S State St at the time the iteration starts
    # at 10:28:40 AM. The package will now go to the Third District Juvenile Court instead of the Council Hall

    df = pd.read_csv("packageinfo.csv")
    df.loc[7, '195 W Oakland Ave'] = '410 S State St'
    df.to_csv("packageinfo.csv", index=False)

    truck_one.insert_regular_package(9, package_with_note)  # Package 9 is inserted into the truck with the updated address
    truck_one.print_individual_package_info()
    exit()
def option_three():
    truck_one = Truck(16, '#1', 0, hubs_ref.get_node_by_index(0), 8, 0, 0)  # Truck #1 starts at Hub Index 0 & leaves at 08:00:00.
    truck_two = Truck(16, '#2', 0, hubs_ref.get_node_by_index(0), 9, 5, 0)  # Truck #2 starts at Hub Index 0 & leaves at 09:05:00 to make sure that all the packages that arrive at 09:05 are sent in this truck
    truck_three = Truck(16, '#3', 0, hubs_ref.get_node_by_index(0), 0, 0, 0)  # Truck #3 is not used

    truck_two_regular_packages = [3, 18, 28]  # Packages that can only be on the Truck #2 & some packages that have to be loaded after 09:05 AM.
    truck_two_priority_packages = [6, 25, 32, 36, 38]  # Packages that have to be together, packages that won't be at the depot till 09:05 AM. Expand this list as required if more priority packages are to be added.
    truck_one_priority_package = [23]

    # Sorts all packages by zip code & holds them all in all_package_list. Later grouped into packages with deadlines & packages with a note
    for packages in packages_ref.group_packages_by_zip().values():
        for package in packages:
            all_package_list.append(package)
    # package_with_deadline holds all the packages with a deadline & removes them from all_package_list if present there
    for package in packages_ref.get_packages_by_deadline():
        if package in all_package_list:
            package_with_deadline.append(package)
            all_package_list.remove(package)
    # package_with_note holds all the packages with a note & any packages still remaining in the all_package_list & removes them from the initial holders if they are present here
    for package in packages_ref.get_packages_by_note():
        if package in all_package_list:
            package_with_note.append(package)
            all_package_list.remove(package)
        if package in package_with_deadline:
            package_with_note.append(package)
            package_with_deadline.remove(package)
    truck_one.insert_regular_package(13, package_with_deadline)
    truck_one.insert_regular_package(14, package_with_note)
    truck_one.insert_regular_package(15, package_with_deadline)
    truck_one.insert_regular_package(16, package_with_note)
    truck_one.insert_regular_package(19, all_package_list)
    truck_one.insert_regular_package(20, package_with_note)
    truck_one.load_priority_packages()  # Load all the packages with 09:00 & 10:30 deadlines
    truck_one.print_package_status()  # Prints whether the regular packages for Truck #1 is delivered or en-route

    for package_numb in truck_two_priority_packages:
        truck_two.insert_priority_package(package_numb, package_with_note)

    for package_numb in truck_two_regular_packages:
        truck_two.insert_regular_package(package_numb, package_with_note)

    truck_two.load_regular_packages()
    truck_two.print_package_status() # Prints whether the regular packages for Truck #2 are delivered or en-route
    truck_one.load_regular_packages()
    # Truck #1 is now on its second iteration
    # The second iteration starts after the 16th package from the Truck 1 is delivered and the truck returns back to WGU
    # The second iteration starts at 10:28:40 AM which is after the address of the package 9 is declared at 10:20 AM
    # The code below changes the address of package 9 from 195 W Oakland Ave to 410 S State St at the time the iteration starts
    # at 10:28:40 AM. The package will now go to the Third District Juvenile Court instead of the Council Hall

    df = pd.read_csv("packageinfo.csv")
    df.loc[7, '195 W Oakland Ave'] = '410 S State St'
    df.to_csv("packageinfo.csv", index=False)

    truck_one.insert_regular_package(9, package_with_note)
    truck_one.print_individual_package_info()
    exit()

if selected_option == '1':
    option_one()
if selected_option == '2':
    option_two()
if selected_option == '3':
    option_three()
if selected_option == '4':
    exit()
