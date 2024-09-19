
import csv
from locations import Location
from nodes import Nodes
from package import Package
from package import Packages
from hashtable import HashMap


hubs_ref = Nodes()
packages_ref = Packages()

# Read the data values from input_data.csv seprated by a comma.
with open('inputdata.csv') as csvfile:
    read_csv = csv.reader(csvfile, delimiter=',')

    hash_ref = HashMap()  # Create an instance of HashMap class

    # Insert values from csv file into key/value pairs of the hash table
    # The ID of the package is the key
    for row in read_csv:
        id = row[0]
        address = row[1]
        delivery = row[2]
        size = row[3]
        note = row[4]
        delivery_status = row[5]
        value = [id, address, delivery, size, note, delivery_status]
        key = id
        hash_ref.insert_val(key, value)
    def get_hash_map():
        return hash_ref

# Index is the key, Hub details are the val.
with open('distances.csv') as distance_csv:
    read_csv = csv.reader(distance_csv, delimiter=',')
    for index, val in enumerate(read_csv):
        h = Location(index, val[0], val[1], val[2], val[3:])
        hubs_ref.add_node(h)

# Uses the append package method to append a package from packageinfo.csv. The package is accessible through packages_ref reference variable
# The package index is column 0
with open('packageinfo.csv') as package_csv:
    read_csv = csv.reader(package_csv, delimiter=',')
    for package in read_csv:
        p = Package(package[0], package[1], package[2], package[3], package[4], package[5], package[6], package[7])
        packages_ref.append_package(p)
for hub in hubs_ref.node_list:
    for adjacent_hub in hubs_ref.node_list:
        hubs_ref.init_undirected_edge(hub, adjacent_hub, hub.neighbors[adjacent_hub.index])


all_package_list = []
packages_delivered_list = []
package_with_deadline = []
id_of_this_package = []
package_with_note = []
package_nine = []
