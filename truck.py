import operator
from operator import attrgetter
from csvreader import hubs_ref
from csvreader import packages_ref
from csvreader import package_with_note
from csvreader import all_package_list, delivery_status
from csvreader import package_with_deadline
from csvreader import packages_delivered_list
from locations import Location
from csvreader import get_hash_map
from hashtable import HashMap


class Truck(Location):
    def __init__(self, max_packages, truck_name, mileage, location, hours, minutes, seconds):
        self.regular_current_packages = []
        self.priority_current_packages = []
        self.priority_current_route = []
        self.regular_current_route = []
        self.max_packages = max_packages
        self.name = truck_name
        self.mileage = mileage
        self.location = location
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds



    # Insert function
    def insert_regular_package(self, package, delivery_list):
        if (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
            self.regular_current_packages.append(str(package))
            delivery_list.remove(str(package))
        else:
            print('Truck full')

    # Insert function
    def insert_priority_package(self, package, delivery_list):
        if (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
            self.priority_current_packages.append(str(package))
            delivery_list.remove(str(package))
        else:
            print('Truck full ')

    # Remove function
    def remove_package(self, package):
        package_with_note.append(package)
        if package in self.regular_current_packages:
            self.regular_current_packages.remove(package)
        if package in self.priority_current_packages:
            self.priority_awaiting_delivery_list.remove(package)

    # Checks if there are regular packages awaiting delivery. If there are packages waiting, checks if there is room
    # in the truck. If there is, loads from the back end of the list until the truck is full or the list is empty.
    def load_regular_packages(self):
        if len(all_package_list) > 0:
            while (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
                try:
                    self.regular_current_packages.append(all_package_list.pop())
                except IndexError:
                    break

    # Checks if there are priority packages awaiting delivery. If there are packages waiting, checks if there is room
    # in the truck. If there is, loads from the back end of the list until the truck is full or the list is empty.
    def load_priority_packages(self):
        if len(package_with_deadline) > 0:
            while (len(self.regular_current_packages) + len(self.priority_current_packages)) < self.max_packages:
                try:
                    self.priority_current_packages.append(package_with_deadline.pop())
                except IndexError:
                    break

    # For each package in truck, checks each package delivery address for matching hub address and adds that hub
    # to a list of hubs_ref that will be delivered to. Called every time a truck is loaded, and when a delivery to a hub
    # is made.
    def create_route(self):
        for priority_package in self.priority_current_packages:
            for hub in hubs_ref.node_list:
                if packages_ref.get_package_address_by_id(str(priority_package)) == \
                        hubs_ref.get_node_address_by_id(hub.index):
                    if hub not in self.priority_current_route:
                        self.priority_current_route.append(hub)
        for regular_package in self.regular_current_packages:
            for hub in hubs_ref.node_list:
                if packages_ref.get_package_address_by_id(str(regular_package)) == \
                        hubs_ref.get_node_address_by_id(hub.index):
                    if hub not in self.regular_current_route:
                        self.regular_current_route.append(hub)

    # Check to see if current hub is in route. If it is, it has been visited and is removed from the route.
    def remove_hub_from_route(self):
        for hub in self.priority_current_route:
            if hub == self.location:
                self.priority_current_route.remove(hub)
        for hub in self.regular_current_route:
            if hub == self.location:
                self.regular_current_route.remove(hub)


    def time_between_hubs(self, miles):
        total_seconds = (miles * 3600) / 18  # Total number of seconds
        self.seconds = (self.seconds + total_seconds) % 60  # Computes seconds on clock
        minutes_remainder = total_seconds / 60  # Variable is now remaining minutes
        self.minutes = (self.minutes + minutes_remainder) % 60  # Computes minutes on clock
        hours_remainder = minutes_remainder / 60  # Variable is now remaining hours
        self.hours = (self.hours + hours_remainder)

    # Main Dijkstra
    # Creates a list of all the unvisited nodes & then assigns the lowest of them as the current node
    # Distance from the current hub to the adjacent hub is the edge_weight
    # If the alternate path is shorter, make the alternate path distance as the baseline & make the alternate node as the current location & traverse from there

    def dijkstra_main_alg(self, hubs_ref, start_hub):
        self.clean_dijkstra_distances()
        unvisited_nodes = [] # Initiate an array-based priority queue
        for current_hub in hubs_ref.adjacent_nodes:
            unvisited_nodes.append(current_hub)
        start_hub.distance = 0
        while len(unvisited_nodes) > 0:
            smallest_index = 0
            for i in range(1, len(unvisited_nodes)):
                if unvisited_nodes[i].distance < unvisited_nodes[smallest_index].distance:
                    smallest_index = i
            current_hub = unvisited_nodes.pop(smallest_index)

            for adj_hub in hubs_ref.adjacent_nodes[current_hub]:
                edge_weight = float(hubs_ref.distance_to_node[(current_hub, adj_hub)])
                alternate_path_distance = current_hub.distance + edge_weight

                if alternate_path_distance < adj_hub.distance:
                    adj_hub.distance = alternate_path_distance
                    adj_hub.previous_location = current_hub


    def clean_dijkstra_distances(self):
        for hub in hubs_ref.node_list:
            hub.distance = float('inf')


    # Main front-end display method. Appends all the hubs in their respective priority or regular categories and creates a route.
    # It then applies the dijkstra. Gets the closest hub from the current hub & prints the respective info for the package/s that belong there.
    def deliver_route(self):
        while (len(self.regular_current_packages) or len(self.priority_current_packages)) != 0:
            self.create_route()
            self.dijkstra_main_alg(hubs_ref, self.location)
            print('\nTruck ' + str(self.name) + ' left the location: ' + str(self.location.name) + "\033[0m  (Address: " + str(self.location.address) + ")")
            print('Truck is now in transit')
            self.remove_hub_from_route()
            if len(self.priority_current_route) > 0:
                next_delivery = min(self.priority_current_route, key=attrgetter('distance')) # If destinations remaining in priority route, get the distance to the next one.
            elif len(self.regular_current_route) > 0:
                next_delivery = min(self.regular_current_route, key=attrgetter('distance')) # If destinations remaining in regular route, get the distance to the next one
            print('Truck ' + str(self.name) + ' has arrived at location: ' + str(next_delivery.name))
            print('Currently Truck ' + str(self.name) + ' is at location: ' + str(next_delivery.name))
            self.time_between_hubs(next_delivery.distance)
            self.mileage += next_delivery.distance
            print('Miles Traveled: ' + str(next_delivery.distance), end='\n')
            hrs = str(int(self.hours))
            mins = str(int(self.minutes))
            secs = str(int(self.seconds))

            time_of_delivery_of_this_package = (hrs + ': ' + mins + ': ' + secs)
            print('Current Mileage of This truck: ' + str(self.mileage),end='\n')
            print('\033[1mPackages with status: DELIVERED: ' + str(packages_delivered_list),end='\n'"\033[0m")
            self.location = next_delivery
            priority_new_package_list = [] # List of packages that still need to be delivered
            regular_new_package_list = [] # List of packages that still need to be delivered
            priority_packages_delivered_at_hub = [] # List of packages that have already been delivered
            regular_packages_delivered_at_hub = [] # List of packages that have already been delivered

            # After every package is delivered, the code below categorizes every package in one of the 3 categories:
            # At the Hub, Delivered or En Route. With every delivery, it updates & then displays the packages in their
            # corresponding categories

            for package in self.priority_current_packages:

                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    priority_new_package_list.append(package) # Added to the list of the packages left to deliver
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    priority_packages_delivered_at_hub.append(package) # Added to the list of the packages delivered

            for package in self.regular_current_packages:
                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    regular_new_package_list.append(package) # Added to the list of the packages left to deliver
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    regular_packages_delivered_at_hub.append(package) # Added to the list of the packages delivered

            self.priority_current_packages = priority_new_package_list # Update the new TBD list
            self.regular_current_packages = regular_new_package_list # Update the new TBD list

            # Display the list of the packages in their corresponding categories in the GUI in an interactive manner.
            def convert_integers_to_strings(int_list):
                return [str(num) for num in int_list]

            integer_list = list(range(1, 41))  # Total packages. Range bound can be changed as more packages are added
            string_list = convert_integers_to_strings(integer_list)
            package_hub_list = []
            for i in string_list:
                if i not in packages_delivered_list :
                    if i not in self.priority_current_packages:
                        if i not in self.regular_current_packages:
                          package_hub_list.append(i)
            print('\033[1mPackages with status: AT THE HUB: ', package_hub_list,end='\n'"\033[0m")

            for i in priority_packages_delivered_at_hub:
                if len(i) > 1:
                    packages_delivered_list[-1:][0]
                    print('Truck just delivered Package ID # ', i, 'at ',time_of_delivery_of_this_package, 'at ', str(self.location.address),
                          end='\n')
                    print('\033[1mPackages with status: STILL EN ROUTE :' + '  '+ str(self.regular_current_packages) + str(
                        self.priority_current_packages),end='\n'"\033[0m")
                    print('\n\n\n\n\n\n-------------------------------------------------------------------------------------------------')
                    print('\n\n\n')
                else:
                    packages_delivered_list[-1:][0]
                    print('Truck just delivered Package ID # ', i, 'at ',time_of_delivery_of_this_package, 'at ', str(self.location.address),
                          end='\n')
                    print('\033[1mPackages with status: STILL EN ROUTE :' + '  '+ str(self.regular_current_packages) + str(
                        self.priority_current_packages),end='\n'"\033[0m")
                    print('\n\n\n\n\n\n-------------------------------------------------------------------------------------------------')
                    print('\n\n\n')

            for i in regular_packages_delivered_at_hub:
                if len(i) > 1:
                    packages_delivered_list[-1:][0]
                else:
                    packages_delivered_list[-1:][0]
                print('Truck just delivered Package ID # ', i, 'at ',time_of_delivery_of_this_package, 'at ', str(self.location.address),
                      end='\n')
                print('\033[1mPackages with status: STILL EN ROUTE :' + '  '+ str(self.regular_current_packages) + str(
                        self.priority_current_packages),end='\n'"\033[0m")
                print('\n\n\n\n\n\n-------------------------------------------------------------------------------------------------')
                print('\n\n\n')

        self.return_to_first_hub()


    # Option #2. If the user chooses this option, the alg goes through the same code to derive the same route as option 1
    # The alg then prints individual package info by utilizing the get_hash_map method from the hash table created in hashtable.py
    def print_individual_package_info(self):
        while (len(self.regular_current_packages) or len(self.priority_current_packages)) != 0:
            self.create_route()
            self.dijkstra_main_alg(hubs_ref, self.location)
            self.remove_hub_from_route()
            if len(self.priority_current_route) > 0:
                next_delivery = min(self.priority_current_route, key=attrgetter(
                    'distance'))  # If destinations remaining in priority route, get the distance to the next one.
            elif len(self.regular_current_route) > 0:
                next_delivery = min(self.regular_current_route, key=attrgetter(
                    'distance'))  # If destinations remaining in regular route, get the distance to the next one
            self.time_between_hubs(next_delivery.distance)
            self.mileage += next_delivery.distance
            hrs = str(int(self.hours))
            mins = str(int(self.minutes))
            secs = str(int(self.seconds))

            time_of_delivery_of_this_package = (hrs + ': ' + mins + ': ' + secs)
            self.location = next_delivery
            priority_new_package_list = []  # List of packages that still need to be delivered
            regular_new_package_list = []  # List of packages that still need to be delivered
            priority_packages_delivered_at_hub = []  # List of packages that have already been delivered
            regular_packages_delivered_at_hub = []  # List of packages that have already been delivered

            for package in self.priority_current_packages:

                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    priority_new_package_list.append(package)  # Added to the list of the packages left to deliver
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    priority_packages_delivered_at_hub.append(package)  # Added to the list of the packages delivered

            for package in self.regular_current_packages:
                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    regular_new_package_list.append(package)  # Added to the list of the packages left to deliver
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    regular_packages_delivered_at_hub.append(package)  # Added to the list of the packages delivered

            self.priority_current_packages = priority_new_package_list  # Update the new TBD list
            self.regular_current_packages = regular_new_package_list  # Update the new TBD list
            id_of_this_package = []
            for i in priority_packages_delivered_at_hub:
                if len(i) > 1:
                    packages_delivered_list[-1:][0]

                    print('Package ID ', i, 'at ', str(self.location.name))
                else:
                    packages_delivered_list[-1:][0]

                    print('Package ID ', i, 'at ', str(self.location.name))

            for i in regular_packages_delivered_at_hub:
                if len(i)>1:
                    packages_delivered_list[-1:][0]
                else:
                    packages_delivered_list[-1:][0]

                print('Package ID ', i, 'at ', str(self.location.name))


            id_of_this_package = packages_delivered_list[-1:][0]
            try:
                inp_skip = input('\n Press 0 to skip this package. \n Press 1 if there are multiple packages delivered at the same location & u want to know the package info of one of them.\n Press 2 if there is only one package delivered at this location & you want to know the package info\n\n ')
                if int(inp_skip) == 0:
                    print('You have skipped this package. Select an option for the next package')
                elif int(inp_skip) == 1:
                    try:
                        inp_id = input('Type the ID of the package you would like to know the info about: \n\n')
                        print(
                            f'Package ID: {get_hash_map().get_val(str(inp_id))[0]}\n'
                            f'Street address: {get_hash_map().get_val(str(inp_id))[1]}\n'
                            f'Required delivery time: {get_hash_map().get_val(str(inp_id))[2]}\n'
                            f'Package weight: {get_hash_map().get_val(str(inp_id))[3]} kilos \n'
                            f'Package Note: {get_hash_map().get_val(str(inp_id))[4]}\n'
                            f'Arrival time: {time_of_delivery_of_this_package}\n\n\n')
                    except ValueError:
                        print('Not the correct Package ID')



                elif int(inp_skip) == 2:

                        print(
                f'Package ID: {get_hash_map().get_val(str(id_of_this_package))[0]}\n'
                f'Street address: {get_hash_map().get_val(str(id_of_this_package))[1]}\n'
                f'Required delivery time: {get_hash_map().get_val(str(id_of_this_package))[2]}\n'
                f'Package weight: {get_hash_map().get_val(str(id_of_this_package))[3]} kilos \n'
                f'Package Note: {get_hash_map().get_val(str(id_of_this_package))[4]}\n'
                f'Arrival time: {time_of_delivery_of_this_package}\n\n\n')

            except ValueError:
                print('Error executing code')

    # 3rd option. Prints the package status at the time the user inputs
    # The alg runs the same code to derive the same route as options 1 & 2. The alg then compares the time input by the user
    # to the time the package/s arrives
    def print_package_status(self):

        while (len(self.regular_current_packages) or len(self.priority_current_packages)) != 0:  # Check for packages
            self.create_route()
            self.dijkstra_main_alg(hubs_ref, self.location)
            self.remove_hub_from_route()
            if len(self.priority_current_route) > 0:
                next_delivery = min(self.priority_current_route, key=attrgetter('distance'))
            elif len(self.regular_current_route) > 0:
                next_delivery = min(self.regular_current_route, key=attrgetter('distance'))
            self.time_between_hubs(next_delivery.distance)
            self.mileage += next_delivery.distance
            hrs = int(self.hours)
            mins = int(self.minutes)
            secs = int(self.seconds)


            time_of_delivery_of_this_package = hrs, ':',mins, ':', secs


            self.location = next_delivery
            priority_new_package_list = []
            regular_new_package_list = []
            priority_packages_delivered_at_hub = []
            regular_packages_delivered_at_hub = []
            for package in self.priority_current_packages:
                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    priority_new_package_list.append(package)
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    priority_packages_delivered_at_hub.append(package)
            for package in self.regular_current_packages:
                if packages_ref.get_package_address_by_id(str(package)) != self.location.address:
                    regular_new_package_list.append(package)
                elif packages_ref.get_package_address_by_id(str(package)) == self.location.address:
                    packages_delivered_list.append(package)
                    regular_packages_delivered_at_hub.append(package)
            self.priority_current_packages = priority_new_package_list
            self.regular_current_packages = regular_new_package_list

            id_of_this_package = packages_delivered_list[-1:][0]
            print("\033[1m" + 'ID of the package: ', id_of_this_package,
                      end='\n'"\033[0m")
            arrival_of_this_package = (time_of_delivery_of_this_package)
            # The user inputs the H:M:S. The alg compares if the package's arriving H:M:S is less, more or equal to the input H:M:S
            # If it is less, then the package is already delivered. If it is equal or more, then the package is either en-route or at the hub
            try:
                inp_skip = input('Press 0 to skip this package or Press 1 to know this package status at a particular time\n')
                if int(inp_skip) == 0:
                    print('You have skipped this package. Select an option for the next package')
                elif int(inp_skip) == 1:
                    try:
                       inp_hrs = input('Enter HOUR: ')
                       inp_mins = input('Enter MINUTE: ')
                       inp_secs = input('Enter SECOND: ')
                       if int(inp_hrs) > int(hrs):
                         print('Status: Package', id_of_this_package, ' already Delivered before', inp_hrs, ":", inp_mins, ":", inp_secs)
                         print('This package arrived at ', arrival_of_this_package)
                       if int(inp_hrs) < int(hrs):
                         print('Status: Package ', id_of_this_package, ' still at the hub at', inp_hrs, ":", inp_mins, ":", inp_secs)
                         print('This package will arrive at ', arrival_of_this_package)
                       if int(inp_hrs) == int(hrs):
                        if int(inp_mins) == int(mins):
                         if int(inp_secs) > int(secs):
                            print('Status: Package', id_of_this_package, ' already Delivered before', inp_hrs, ":", inp_mins, ":", inp_secs)
                            print('This package arrived at ', arrival_of_this_package)
                        elif int(inp_secs) < int(secs):
                            print('Status: Package ', id_of_this_package, ' EN ROUTE at', inp_hrs, ":", inp_mins, ":", inp_secs)
                            print('This package will arrive at ', arrival_of_this_package)
                        elif int(inp_mins) > int(mins):
                         print('Status: Package', id_of_this_package, ' already Delivered before', inp_hrs, ":", inp_mins, ":", inp_secs)
                         print('This package arrived at ', arrival_of_this_package)
                        elif int(inp_mins) < int(mins):
                         print('Status: Package ', id_of_this_package, ' EN ROUTE at', inp_hrs, ":", inp_mins, ":", inp_secs)
                         print('This package will arrive at ', arrival_of_this_package)
                    except ValueError:
                        print('Invalid')
            except ValueError:
                print('Error executing code')






    # Utilize dijkstras algorithm to get back to WGU, the first starting point. Can be expanded for any other starting point/s.
    def return_to_first_hub(self):
        self.dijkstra_main_alg(hubs_ref, self.location)
        print('\nAll Packages delivered by Truck ' + str(self.name) + '. Returning to WGU from ' +
              str(self.location.name))
        print('Distance from WGU = ' + str(hubs_ref.get_node_by_index(0).distance))
        print('Driving from : ' + str(self.location.name))
        print('Driving to : ' + str(hubs_ref.get_node_by_index(0).name))
        self.time_between_hubs(hubs_ref.get_node_by_index(0).distance)
        self.mileage += hubs_ref.get_node_by_index(0).distance
        print('Miles Traveled: ' + str(hubs_ref.get_node_by_index(0).distance))
        print('Time of Arrival: ' + str(int(self.hours)) + ': ' + str(int(self.minutes)) + ': '
              + str(int(self.seconds)))
        print('Total Mileage of this truck: ' + str(self.mileage))
        print('Packages Delivered Today: ' + str(packages_delivered_list))
        self.location = hubs_ref.get_node_by_index(0)
        print('Arrived at ' + str(self.location.name))


