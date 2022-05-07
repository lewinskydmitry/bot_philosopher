from vm.MyVendingMachine import MyVendingMachine
from vm.MyVendingMachineBuilder import MyVendingMachineBuilder
from vm.MyVeryBestVendingMachineBuilder import MyVeryBestVendingMachineBuilder

# instantiating machine
builder1 = MyVendingMachineBuilder()
builder2 = MyVeryBestVendingMachineBuilder()

myMachine = builder1.build(MyVendingMachine())
myMachine2 = builder2.build(MyVendingMachine())

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
