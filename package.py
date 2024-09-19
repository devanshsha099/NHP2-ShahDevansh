

# Package class holds all the package information.
class Package:
    def __init__(self, package_id, package_address, city, state, package_zip_code, deadline, mass, note):
        self.package_id = package_id
        self.address = package_address
        self.city = city
        self.state = state
        self.zip_code = package_zip_code
        self.deadline = deadline
        self.mass = mass
        self.note = note

class Packages:
    def __init__(self):
        self.package_list = [] # Create a package list to be displayed in the interface
        pass

    # Add a note to the package to later distinguish it
    def append_note(self, package, input):
        from csvreader import packages_ref
        packages_ref.get_package(package - 1).note = str(input)

    # Attach the package to the package list created initially
    def append_package(self, package_to_append):
        self.package_list.append(package_to_append)

    # Get a package from the list based on its index in the list
    def get_package(self, index):
        return self.package_list[index]

    # Return a list of all the packages with a deadline
    def get_packages_by_deadline(self):
        packages_by_deadline = []
        for row in range(len(self.package_list)):
            if self.package_list[row].deadline != 'EOD':
                packages_by_deadline.append(self.package_list[row].package_id)
        if len(packages_by_deadline) > 0:
            return packages_by_deadline
        else:
            return None

    # Group all the packages that belong to a specific zip code & do this for all the zip codes
    def group_packages_by_zip(self):
        packages_grouped_by_zip = {}
        for row in range(len(self.package_list)):
            packages_grouped_by_zip.setdefault(self.package_list[row].zip_code,
                                               []).append(self.package_list[row].package_id)
        if len(packages_grouped_by_zip) > 0:
            return packages_grouped_by_zip
        else:
            return None

    # Goes through all 40 rows & holds the packages with their zip codes.
    def get_packages_by_note(self):
        packages_by_note = []
        from csvreader import packages_ref
        for package in packages_ref.package_list:
            if len(package.note) > 2:
                packages_by_note.append(package.package_id)
        if len(packages_by_note) > 2:
            return packages_by_note
        else:
            return None


    # Attach a package ID to the address it belongs
    def get_package_address_by_id(self, package_id):
        for row in range(len(self.package_list)):
            if self.package_list[row].package_id == package_id:
                return self.package_list[row].address
