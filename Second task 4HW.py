import copy
class VendingMachine:

    def __init__(self):
        # means of payment - coin and bill types
        # first tuple item: value in cents. Second: if it can be returned to user as a change?
        # defined on factory and can not be altered by operator
        self.__coin1c = (1, True)
        self.__billS20 = (2000, False)
        self.__coin5c = (5, True)
        self.__coin10c = (10, True)
        self.__coin25c = (25, True)
        self.__billS1 = (100, True)
        self.__billS5 = (500, False)
        self.__billS10 = (1000, False)

        # shelfs and their capacities are defined on factory and can not be altered by operator
        self.__inventory_shelves = (0, 1, 2, 3, 4, 5, 6, 7)
        self.__inventory_shelves_capacity = (70, 60, 60, 60, 60, 60, 60, 60)
        assert(len(self.__inventory_shelves) == len(self.__inventory_shelves_capacity))

        self.__cashier = dict()
        self.__vending_items = set()
        self.__inventory = dict()
        self.__purchases = dict()

        self.__reset()

    @property
    def coin1c(self):
        return self.__coin1c

    @property
    def coin5c(self):
        return self.__coin5c

    @property
    def coin10c(self):
        return self.__coin10c

    @property
    def coin25c(self):
        return self.__coin25c

    @property
    def billS1(self):
        return self.__billS1

    @property
    def billS5(self):
        return self.__billS5

    @property
    def billS10(self):
        return self.__billS10

    @property
    def billS20(self):
        return self.__billS20

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
    def addInventory(self, shelf, vending_item, quantity):

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

    # use case #2.A - Vendor gets a report on which items are left in the machine
    @property
    def inventory(self):
        return self.__inventory

    # use case #3.A - Vendor gets a report on money in the machine' cashier
    @property
    def cashier(self):
        return self.__getAmountOfCash(), self.__cashier

    # use case #3 - Vendor fills the machine with coins for change
    @cashier.setter
    def cashier(self, value):
        self.__cashier = value

    # use case #3.B - Vendor takes money from the machine' cashier
    def substractMoneyFromCashier(self, paymentMethod, quantity):
        if cashier[paymentMethod] < quantity or quantity <= 0:
            return False
        else:
            cashier[paymentMethod] -= quantity  # 250 dollars withdrawn
            return True

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

    # use case #4 - User purchases an item from shelf
    # we will assume that user
    def purcaseItem(self, shelfNumber, payments):
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
        return self.__getAmountOfCash() < other.__getAmountOfCash()

    def __le__(self, other):
        return self.__getAmountOfCash() <= other.__getAmountOfCash()

    def __eq__(self, other):
        return self._getAmountOfCash() == other._getAmountOfCash()

    def __ne__(self, other):
        return self._getAmountOfCash() != other._getAmountOfCash()

    def __gt__(self, other):
        return self.__getAmountOfCash() > other.__getAmountOfCash()

    def __ge__(self, other):
        return self.__getAmountOfCash() >= other.__getAmountOfCash()

    def __getAmountOfCash(self):

        amount = 0
        monetary_items = (
            self.__coin1c,
            self.__coin5c,
            self.__coin10c,
            self.__coin25c,
            self.__billS1,
            self.__billS5,
            self.__billS10,
            self.__billS20
        )
        for monetary_item in monetary_items:
            amount += self.__cashier[monetary_item] * monetary_item[0]

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
        combined_vending_machine = VendingMachine()
        combined_vending_machine.__vending_items.update(self.__vending_items)
        combined_vending_machine.__vending_items.update(other.__vending_items)

        shelf = 0
        for inventory_item in all_inventory:
            if shelf not in combined_vending_machine.__inventory_shelves:
                combined_vending_machine.__inventory_shelves = range(shelf)
                combined_vending_machine.__inventory_shelves_capacity = (list(combined_vending_machine.__inventory_shelves_capacity), all_inventory[inventory_item])
            combined_vending_machine.addInventory(shelf, inventory_item, all_inventory[inventory_item])
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
        combined_vending_machine = VendingMachine()
        combined_vending_machine.__vending_items.update(self.__vending_items)
        combined_vending_machine.__vending_items.update(other.__vending_items)

        shelf = 0
        for inventory_item in intersection_inventory:
            if shelf not in combined_vending_machine.__inventory_shelves:
                combined_vending_machine.__inventory_shelves = range(shelf)
                combined_vending_machine.__inventory_shelves_capacity = (list(combined_vending_machine.__inventory_shelves_capacity), intersection_inventory[inventory_item])
            combined_vending_machine.addInventory(shelf, inventory_item, intersection_inventory[inventory_item])
            shelf += 1

        return combined_vending_machine
#######################################################################################################################

#
# Operator-side use cases - machine management
#
# instantiating machine
myMachine = VendingMachine()

# operator defined what vending items the machine will be capable to sell
mars = ("Mars bar", 200)
snickers = ("Snickers bar", 200)
snickersXXL = ("Snickers XXL bar", 200)
bounty = ("Bounty bar", 200)
coke = ("Can of Coke", 150)
dietCoke = ("Can of Diet Coke", 150)
pythonBook = ("Python for Convex Problems", 506)  # yes, it is expensive!
vending_items = set()
vending_items.add(mars)
vending_items.add(snickers)
vending_items.add(snickersXXL)
vending_items.add(bounty)
vending_items.add(coke)
vending_items.add(dietCoke)
vending_items.add(pythonBook)
myMachine.provision(vending_items)

# operator loads vending items to the machine
myMachine.addInventory(0, mars, 30)
myMachine.addInventory(1, mars, 5)
myMachine.addInventory(2, mars, 15)
myMachine.addInventory(3, snickers, 10)
myMachine.addInventory(4, bounty, 10)
myMachine.addInventory(5, coke, 10)
myMachine.addInventory(6, dietCoke, 5)
myMachine.addInventory(7, pythonBook, 1)
#myMachine.addInventory(8, dietCoke, 5)  # fail - no such shelf

# operator gets report on what items were loaded into machine
print(f"Machine vending items are: {myMachine.inventory}")

# operator loads the machine with coins
# machine need coins for change, because credit cards are not invented yet
cashier = dict()
cashier[myMachine.coin1c] = 500
cashier[myMachine.coin5c] = 200
cashier[myMachine.coin10c] = 100
cashier[myMachine.coin25c] = 200
cashier[myMachine.billS1] = 5
cashier[myMachine.billS5] = 0
cashier[myMachine.billS10] = 0
cashier[myMachine.billS20] = 0

myMachine.cashier = cashier
# suppressing all HW 3 tests
'''

# operator collects bills (after some time the machine was used)
# attempt to withdrawn 250 dollars - fail
myMachine.substractMoneyFromCashier(myMachine.billS5, 50)

# attempt to withdrawn 100 dollars - fail
myMachine.substractMoneyFromCashier(myMachine.billS10, 10)
###############################################################################
###############################################################################
###############################################################################
###############################################################################
#
# User side use cases including a few negative cases
#
# User wants to purchase an item from shelf
# TC 1
myMachine.purcaseItem(77, {myMachine.coin25c: 1})  # fail - vending item is not found

# TC 2
myMachine.purcaseItem(7, {myMachine.billS20: 50})  # fail - can not find exact change to return

# TC 3
myMachine.purcaseItem(7, {myMachine.coin25c: 1})  # fail - payment is not enough

# TC 4 - user wants to purchase a Python book
# if the two belows prints are enabled you will see the cashier state before and after purchase
myMachine.purcaseItem(7, {myMachine.billS10: 1})  # SUCCESS!

# TC 5
myMachine.purcaseItem(7, {myMachine.billS10: 1})  # fail - out of stock

print(f"Machine cash is $ {myMachine.cashier[0]}, cons/bills are: {myMachine.cashier[1]}")
'''
#####################################################
# HW4 specific code
# provisioning of the second machine
myMachine2 = VendingMachine()

cashier2 = dict()
cashier2[myMachine.coin1c] = 500
cashier2[myMachine.coin5c] = 200
cashier2[myMachine.coin10c] = 100
cashier2[myMachine.coin25c] = 200
cashier2[myMachine.billS1] = 5
cashier2[myMachine.billS5] = 0
cashier2[myMachine.billS10] = 0
cashier2[myMachine.billS20] = 0

myMachine2.cashier = cashier2
myMachine2.provision(vending_items)
myMachine2.addInventory(1, mars, 10)
myMachine2.addInventory(2, mars, 10)
myMachine2.addInventory(3, snickers, 10)
myMachine2.addInventory(4, bounty, 10)
myMachine2.addInventory(5, coke, 10)
myMachine2.addInventory(6, dietCoke, 10)
myMachine2.addInventory(7, pythonBook, 10)

# HW4 Task 1. Get vending machines content union/intersection
print("Machine 1 inventory:", myMachine.inventory)
print("Machine 2 inventory:", myMachine2.inventory)
union = myMachine + myMachine2
print("Machine 1 & 2 inventory union:", union.inventory)
intersection = myMachine - myMachine2
print("Machine 1 & 2 inventory intersection:", intersection.inventory)

# HW4 Task 2. Compare vending machines by the amount of cash inside (A > B = True)
print(f"Machine 1 cash is $ {myMachine.cashier[0]}, cons/bills are: {myMachine.cashier[1]}")
print(f"Machine 2 cash is $ {myMachine2.cashier[0]}, cons/bills are: {myMachine2.cashier[1]}")

print(f"Machine 1 has more cash than Machine 2 ? {myMachine > myMachine2}")
print(f"Machine 1 has less cash than Machine 1 ? {myMachine < myMachine2}")
