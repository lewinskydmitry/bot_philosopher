from vm.VendingMachine import VendingMachine


class MyVendingMachine(VendingMachine):

    def __init__(self):
        super().__init__()

        # shelfs and their capacities are defined on factory and can not be altered by operator
        self.__inventory_shelves = (0, 1, 2, 3, 4, 5, 6, 7)
        self.__inventory_shelves_capacity = (70, 60, 60, 60, 60, 60, 60, 60)
        assert(len(self.__inventory_shelves) == len(self.__inventory_shelves_capacity))

        self.__cashier = dict()
        self.__vending_items = set()
        self.__inventory = dict()
        self.__purchases = dict()
        self.__reset()

    # use case #1 - Vendor defines which goods will be on sale and their prices
    # this is not quality of goods
    # registered vending items
    # first element of tuple: description of the item
    # second element of tuple: cost of the item in cents
    def provision(self, vending_items):
        self.__vending_items = vending_items

    # use case #2 - Vendor fills the machine with items
    # index - shelf number
    # value - 2 index array - vending item type and number of loaded items
    def add_inventory(self, shelf, vending_item, quantity):

        if shelf not in self.__inventory_shelves:
            #unknows shelf
            print("cant add item to unknown shelf")
            return False

        if shelf not in self.inventory.keys():
            if quantity > self.__inventory_shelves_capacity[shelf]:
                print("cant add item to shelf - exceeding capacity")
                return False
        elif self.inventory[shelf][1] + quantity > self.__inventory_shelves_capacity[shelf]:
            print("cant add item to shelf - exceeding capacity")
            return False

        if vending_item not in self.__vending_items:
            # unknown vendingItem
            print("cant add item to shelf - unknows item")
            return False

        self.inventory[shelf] = [vending_item, quantity]
        return True

    @property
    def inventory(self):
        return self.__inventory

    # use case #3.A - Vendor gets a report on money in the machine' cashier
    @property
    def cashier(self):
        return self.__get_amount_of_cash(), self.__cashier

    # use case #3 - Vendor fills the machine with coins for change
    @cashier.setter
    def cashier(self, value):
        self.__cashier = value

    # use case #3.B - Vendor takes money from the machine' cashier
    def substract_money_from_cashier(self, paymentMethod, quantity):
        if cashier[paymentMethod] < quantity or quantity <= 0:
            return False
        else:
            cashier[paymentMethod] -= quantity
            return True

    # use case #4 - User purchases an item from shelf
    # we will assume that user
    def purchase_item(self, shelfNumber, payments):
        insertedMoney = 0
        for payment in payments.keys():
            insertedMoney += payment[0]*payments[payment]

        if shelfNumber not in self.__inventory_shelves:
            print("Unknown shelf")
            return False

        good = self.inventory[shelfNumber]
        # the system checks if the requested item is available (is in stock)
        if good[1] <= 0:
            print("Out of stock for the item")
            return False

        if insertedMoney < good[0][1]:
            print("Payment is not enough to purchase the item")
            return False

        # the system detects/shows the cost of the item - $5
        print(f"Inserted {insertedMoney} cents, the cost of the item is {good[0][1]} cents")

        # the system calculates amount of change due:
        changeAmount = insertedMoney - good[0][1]

        # we need to calculate how many coins and their values to be returned
        changeConfiguration = self.__getChangeConfiguration(changeAmount)
        if changeConfiguration is None:
            # in some cases we will have to refuse purchase because we ran out of change
            print("Ran out of change or exact change not possible")
            return False

        # the state of cashier needs to be changed
        # step A - coins for change are marked as withdrawn to user
        if changeConfiguration:
            print("User, take you change:")

        for paymentMethod in changeConfiguration.keys():
            print(f"{paymentMethod[0]} cents x {changeConfiguration[paymentMethod]}")
            cashier[paymentMethod] -= changeConfiguration[paymentMethod]

        if changeConfiguration:
            print(f"Total change: {changeAmount} cents")

        # step B - inserted payment needs to marked as it is in the cashier
        for payment in payments.keys():
            cashier[payment] += payments[payment]

        # the state of inventory is changed - available stock on the shelf #6 is reduced by 1
        good = self.inventory[shelfNumber]
        good[1] = good[1] - 1

        # purchases log is appended with the sold good
        if good[0] in self.__purchases.items():
            self.__purchases[good[0]] += 1
        else:
            self.__purchases[good[0]] = 1

        #print(self.purchases)
        #print(self.cashier)  # transaction is logged
        #print(self.inventory)  # transaction is logged
        return True

    # alg calculates change, minimizing number of coins to be returned
    # this protected function
    def __getChangeConfiguration(self, changeAmount):
        # Alg should return changeConfiguration where
        # key - mean of payment object
        # value - number of coins defined by key to be returned as a change

        changeConfiguration = dict()
        scannedPaymentMethods = set()
        while changeAmount != 0:

            paymentOption, availableAuantity = self.__calculateChange(changeAmount, scannedPaymentMethods)

            if not paymentOption:
                # we ran out of options to find exact change
                return None

            scannedPaymentMethods.add(paymentOption)
            thisRequiredNumber = int(changeAmount / paymentOption[0])
            usedCoins = min(availableAuantity, thisRequiredNumber)
            if not usedCoins:
                continue

            changeAmount -= usedCoins*paymentOption[0]
            changeConfiguration[paymentOption] = usedCoins

        return changeConfiguration

    def __calculateChange(self, amount, scannedPaymentMethods):
        maxAmount = 0
        maxAmountPaymentMethod = None
        for paymentMethod in cashier.keys():
            if paymentMethod not in scannedPaymentMethods and paymentMethod[0] > maxAmount and paymentMethod[1]:
                maxAmount = paymentMethod[0]
                maxAmountPaymentMethod = paymentMethod

        return maxAmountPaymentMethod, cashier[maxAmountPaymentMethod] if maxAmountPaymentMethod else None

    def __lt__(self, other):
        return self.__get_amount_of_cash() < other.__get_amount_of_cash()

    def __le__(self, other):
        return self.__get_amount_of_cash() <= other.__get_amount_of_cash()

    def __eq__(self, other):
        return self.__get_amount_of_cash() == other.__get_amount_of_cash()

    def __ne__(self, other):
        return self.__get_amount_of_cash() != other.__get_amount_of_cash()

    def __gt__(self, other):
        return self.__get_amount_of_cash() > other.__get_amount_of_cash()

    def __ge__(self, other):
        return self.__get_amount_of_cash() >= other.__get_amount_of_cash()

    def __get_amount_of_cash(self):

        amount = 0
        for monetary_item in self.__cashier.keys():
            amount += self.__cashier[monetary_item] * monetary_item.value

        return amount/100

    # union of A and B by inventory
    def __add__(self, other):

        all_inventory = dict()
        for inv in self.inventory:
            if self.inventory[inv][0] in all_inventory and self.inventory[inv][1] > 0:
                all_inventory[self.inventory[inv][0]] += self.inventory[inv][1]
            elif self.inventory[inv][1] > 0:
                all_inventory[self.inventory[inv][0]] = self.inventory[inv][1]

        for inv in other.__inventory:
            if other.__inventory[inv][0] in all_inventory:
                all_inventory[other.__inventory[inv][0]] += other.__inventory[inv][1]
            else:
                all_inventory[other.__inventory[inv][0]] = other.__inventory[inv][1]

        #print(all_inventory)
        combined_vending_machine = MyVendingMachine()
        combined_vending_machine.__vending_items.update(self.__vending_items)
        combined_vending_machine.__vending_items.update(other.__vending_items)

        shelf = 0
        for inventory_item in all_inventory:
            if shelf not in combined_vending_machine.__inventory_shelves:
                combined_vending_machine.__inventory_shelves = range(shelf)
                combined_vending_machine.__inventory_shelves_capacity = (list(combined_vending_machine.__inventory_shelves_capacity), all_inventory[inventory_item])
            combined_vending_machine.add_inventory(shelf, inventory_item, all_inventory[inventory_item])
            shelf += 1

        return combined_vending_machine

    # intersection of A and B by inventory
    def __sub__(self, other):

        inventory_1 = dict()
        for inv in self.inventory:
            if self.inventory[inv][0] in inventory_1 and self.inventory[inv][1] > 0:
                inventory_1[self.inventory[inv][0]] += self.inventory[inv][1]
            elif self.inventory[inv][1] > 0:
                inventory_1[self.inventory[inv][0]] = self.inventory[inv][1]

        inventory_2 = dict()
        for inv in other.__inventory:
            if other.__inventory[inv][0] in inventory_2:
                inventory_2[other.__inventory[inv][0]] += other.__inventory[inv][1]
            else:
                inventory_2[other.__inventory[inv][0]] = other.__inventory[inv][1]

        all_keys = set(inventory_1.keys())
        all_keys.update(set(inventory_2.keys()))
        intersection_inventory = dict()

        for key in all_keys:
            if key in inventory_1 and key in inventory_2:
                intersection_inventory[key] = min(inventory_1[key], inventory_2[key])

        #print(all_inventory)
        combined_vending_machine = MyVendingMachine()
        combined_vending_machine.__vending_items.update(self.__vending_items)
        combined_vending_machine.__vending_items.update(other.__vending_items)

        shelf = 0
        for inventory_item in intersection_inventory:
            if shelf not in combined_vending_machine.__inventory_shelves:
                combined_vending_machine.__inventory_shelves = range(shelf)
                combined_vending_machine.__inventory_shelves_capacity = (list(combined_vending_machine.__inventory_shelves_capacity), intersection_inventory[inventory_item])
            combined_vending_machine.add_inventory(shelf, inventory_item, intersection_inventory[inventory_item])
            shelf += 1

        return combined_vending_machine

    def __reset(self):

        # cashier - current state of funds inside the machine
        # coins and bills along with their quantity
        # key - mean of payment object
        # value - current quantity of coins/bills inside the cashier
        self.__cashier = dict()
        self.__vending_items = set()
        # inventory - current state of machine inventory
        # key: shelf id, it has to be entered by user to purchase the item
        # value - 2-value array: [0] one of the registered vending items (see below),
        # [1] - it's current stock, i.e. how many of them are currently available
        self.__inventory = dict()

        # purchases - purchasing history
        # key: registered vending items
        # value - how many items were sold
        self.__purchases = dict()
