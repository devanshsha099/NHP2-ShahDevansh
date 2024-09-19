
# There are a total of 26 locations the delivery drivers will traverse through after leaving the hub
# These locations all have an ID, name, address, zip code & a list of neighboring locations
# The last param will be utilized in the main dijkstra to create an efficient route
# The rest of the params will be used to display the package status in the GUI

class Location:
    def __init__(self, location_index, location_name, location_address, location_zip, location_neighbors):
        self.index = location_index
        self.name = location_name
        self.address = location_address
        self.zip_code = location_zip
        self.neighbors = location_neighbors
        self.previous_location = ''
        self.distance = float('inf')

