from .constants import RotationType, Axis
from .auxiliary_methods import intersect, set_to_decimal

DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]

#The Item class represents an item with its name, dimensions (width, height, depth), weight, position, and rotation type.
class Item:
    def __init__(self, name, width, height, depth, weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
#The format_numbers() method is used to set the number of decimal places used for the item's dimensions, weight, and the bin's dimensions and maximum weight. 
    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.weight = set_to_decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals
#The string() method is used to generate a string representation of the object, including its name, dimensions, weight, position, rotation type, volume, and maximum weight (for the bin).
    def string(self):
        return "%s(%sx%sx%s, weight: %s) pos(%s) rt(%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.weight,
            self.position, self.rotation_type, self.get_volume()
        )
#The get_volume() method is used to calculate the volume of an item or bin.
    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )
#The get_dimension() method is used to get the dimensions of an item after rotation.
    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension

#The Bin class represents a bin with its name, dimensions (width, height, depth), maximum weight, and list of items.
class Bin:
#__init__(self, name, width, height, depth, max_weight): This method is the constructor of the Bin class. It initializes a new Bin object with a given name, width, height, depth, and maximum weight that it can hold.
    def __init__(self, name, width, height, depth, max_weight):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = []
        self.unfitted_items = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
#format_numbers(self, number_of_decimals): This method takes a float value and formats it to a specified number of decimal places. It is used to ensure that the dimensions and weights of the Bin are presented with a consistent number of decimal places.
    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.max_weight = set_to_decimal(self.max_weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals
#string(self): This method returns a string representation of the Bin object, including its name, dimensions, and maximum weight.
    def string(self):
        return "%s(%sx%sx%s, max_weight:%s) vol(%s)" % (
            self.name, self.width, self.height, self.depth, self.max_weight,
            self.get_volume()
        )
#get_volume(self): This method calculates and returns the volume of the Bin object based on its dimensions.
    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )
#get_total_weight(self): This method returns the current total weight of the Bin object, which is the sum of the weights of all items currently in the Bin.
    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return set_to_decimal(total_weight, self.number_of_decimals)
#The put_item() method of the Bin class is used to place an item into a bin at a specified pivot point. It checks if the item fits within the bin's dimensions and if there is any intersection between the item and other items already in the bin. If the item fits, it is added to the bin's list of items. If it does not fit, it is marked as unfitted.
    def put_item(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.ALL)):
            item.rotation_type = i
            dimension = item.get_dimension()
            if (
                self.width < pivot[0] + dimension[0] or
                self.height < pivot[1] + dimension[1] or
                self.depth < pivot[2] + dimension[2]
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit

                self.items.append(item)

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit

#The Packer class is responsible for adding bins and items and packing items into bins
class Packer:
#__init__(self): This method is the constructor of the Packer class. It initializes a new Packer object.
    def __init__(self):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
#add_bin(self, bin): This method adds a Bin object to the Packer. The Packer will then attempt to pack items into this Bin.
    def add_bin(self, bin):
        return self.bins.append(bin)
#add_item(self, item): This method adds an Item object to the Packer's list of items to be packed.
    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)
#pack_to_bin(self, bin, item): This method attempts to pack a single item into a specified Bin object. It takes a Bin object and an Item object as input, and attempts to place the item into the Bin using the bin's pivot point. If the item fits in the bin, the method returns True and adds the item to the Bin. If the item does not fit, the method returns False and does not modify the Bin.
    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.items:
            response = bin.put_item(item, START_POSITION)

            if not response:
                bin.unfitted_items.append(item)

            return

        for axis in range(0, 3):
            items_in_bin = bin.items

            for ib in items_in_bin:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]

                if bin.put_item(item, pivot):
                    fitted = True
                    break
            if fitted:
                break

        if not fitted:
            bin.unfitted_items.append(item)
#The pack() method in the Packer class is used to pack the items into the available bins. It sorts the bins and items based on their volume and then tries to fit each item into each bin. If the distribute_items flag is set to True, it also removes the packed items from the list of available items. The number_of_decimals argument is used to format the numbers in the output.
    def pack(
        self, bigger_first=False, distribute_items=False,
        number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS
    ):
        for bin in self.bins:
            bin.format_numbers(number_of_decimals)

        for item in self.items:
            item.format_numbers(number_of_decimals)

        self.bins.sort(
            key=lambda bin: bin.get_volume(), reverse=bigger_first
        )
        self.items.sort(
            key=lambda item: item.get_volume(), reverse=bigger_first
        )

        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item)

            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)
