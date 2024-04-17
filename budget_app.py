class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = []

    def deposit(self,amount,description=""):
        form = {"amount" : float(amount), "description" : description}
        self.ledger.append(form)
    
    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            form = {"amount" : -float(amount), "description" : description}   
            self.ledger.append(form)  
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for items in self.ledger:
            item = list(items.values())
            balance = balance + item[0]
        return balance

    def get_withdraw_balance(self):
        balance = 0
        for items in self.ledger:
            item = list(items.values())
            if item[0]<0:
                balance = balance + item[0]
        return balance    

    def transfer(self,amount,destination_category):
        if self.check_funds(amount):
            description = "Transfer to " + destination_category.name
            self.withdraw(amount,description)

            description = "Transfer from " + self.name
            destination_category.deposit(amount,description)
            return True
        else:
            return False

    def check_funds(self,amount):
        return amount <= self.get_balance() 

    def __str__(self):
        displayer = ""
        fline = self.name
        fline = fline.center(30, "*").rstrip()
        displayer = displayer + fline + '\n'

        for items in self.ledger:
            item = list(items.values())
            spart = item[0]
            spart = str('%.2f'%spart)
            fpart = item[1]
            fpart = fpart[: 23].ljust(23)
            spart = spart[: 7].rjust(7)
            displayer = displayer + fpart + spart + "\n"
        displayer = displayer + "Total: " + str('%.2f'%self.get_balance())
        return displayer
                  

def create_spend_chart(categories):
    output = "\nPercentage spent by category\n"
    spent_by_category = [0] * len(categories)
    spent_perc = [0] * len(categories)
    names = []
    len_names = []

    for idx,category in enumerate(categories):
        spent_by_category[idx] = -category.get_withdraw_balance()
        names.append(category.name.title())
        len_names.append(len(category.name.title()))
        
    sum_withdraw = sum(spent_by_category)
    print(sum_withdraw)

    for idx,category in enumerate(categories):
        spent_perc[idx] = (spent_by_category[idx]/sum_withdraw*100)//10*10

    tmp = 100
    while  tmp >= 0:
        output = output.rstrip(" ") + str(tmp).rjust(3) + "|"
        for idx,category in enumerate(categories):
            if spent_perc[idx]>=tmp:
                output = output + " o "
            else:
                output = output + "   "
        output = output + "\n"
        tmp = tmp - 10

    output = output + "    " + "---"*len(categories) + "-" + "\n"
  
    print(names[0][3])
    for i in range(0,max(len_names)):
        output = output + "    "
        for j in range(0,len(names)):
            try:
                output = output + " " + names[j][i]+ " "
            except:
                output = output + "   "
        output = output + " \n"        

    print(len_names)
    print(output)
    #return(spent_by_category)

food = Category("Food")
food.deposit(1000, "deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(1.1, "socks")
clothing.withdraw(12, "skirt")
bath = Category("Auto")
bath.deposit(200, "deposit")
food.transfer(10, food)
bath.withdraw(3.1, "big bath")
bath.withdraw(40, "long bath")

print(food)
print(clothing)

create_spend_chart([food,clothing,bath])


