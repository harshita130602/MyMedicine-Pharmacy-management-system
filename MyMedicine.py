import subprocess as sp
import pymysql
import pymysql.cursors

import uuid 

def getCartId(user):
    
    try:
        query = "SELECT * FROM CUSTOMER WHERE User_id='"+user['User_id']+"'"
        cur.execute(query)

        customer = cur.fetchall()

        if(len(customer)==0):
            return "Invalid"

        return customer[0]['Cart_id']
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        landing()


def addToCart(user, medicine_id):
    try:
        query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+medicine_id+"'"
        cur.execute(query)

        rows = cur.fetchall()

        # print(rows)
        query = "SELECT * FROM CART_ITEM WHERE Medicine_id='"+medicine_id+"'"
        cur.execute(query)

        check_items = cur.fetchall()
        if(len(check_items)!=0):
            print("You already have this item in your cart.")
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)

        print("You are adding", rows[0]['Medicine_name'], "to your cart.")
        quantity = int(input("Enter quantity (or write 999 to go back)> "))
        tmp = sp.call('clear', shell=True)

        if(quantity==999):
            customerDashboard(user)

        while(quantity>10):
            print("You cannot add more than 10 items of this product.")
            quantity = int(input("Enter quantity (or write 999 to go back)> "))
            tmp = sp.call('clear', shell=True)
            if(quantity==999):
                customerDashboard(user)

        while(quantity>rows[0]['Medicine_stock']):
            print("There are only "+str(rows[0]['Medicine_stock'])+" left. Please select your quantity accordingly.")
            quantity = int(input("Enter quantity (or write 999 to go back)> "))
            tmp = sp.call('clear', shell=True)
            if(quantity==999):
                customerDashboard(user)

        if(quantity==999):
            customerDashboard(user)

        cart_id = getCartId(user)
        total_price = quantity*rows[0]['Medicine_price']

        query = "INSERT INTO CART_ITEM (Cart_id, Medicine_id, Quantity, Total_price) VALUES ('"+cart_id+"', '"+medicine_id+"', "+str(quantity)+", "+str(total_price)+")" 
        cur.execute(query)
        print("Added", quantity, "of", rows[0]['Medicine_name'] ,"to Cart")

        query = "SELECT * FROM CART WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        cart = cur.fetchall()

        query = "UPDATE MEDICINE SET Medicine_stock=Medicine_stock-"+str(quantity)+" WHERE Medicine_id='"+medicine_id+"'"
        cur.execute(query)

        
        if(len(cart)==0):
            query = "INSERT INTO CART(Cart_id, Items, Cart_total_price) VALUES ('"+cart_id+"', 1, "+str(total_price)+")"
            cur.execute(query)
            con.commit()
        else:
            query = "SELECT COUNT(*) FROM CART_ITEM WHERE Cart_id='"+cart_id+"'"
            cur.execute(query)
            total_items = cur.fetchall()

            query = "SELECT SUM(Total_price) FROM CART_ITEM WHERE Cart_id='"+cart_id+"'"
            cur.execute(query);
            total_cart_price = cur.fetchall()

            query = "UPDATE CART SET Items="+str(total_items[0]['COUNT(*)'])+", Cart_total_price="+str(total_cart_price[0]['SUM(Total_price)'])+" WHERE Cart_id='"+cart_id+"'"
            cur.execute(query) 
            con.commit()

        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)


def browseProducts(user):

    try:
        query = "SELECT * FROM MEDICINE WHERE Medicine_stock>0"
        cur.execute(query)

        rows = cur.fetchall()

        count = 1;
        for row in rows:
            print(row["Medicine_id"]+".", row['Medicine_name'], '- Rs.', row['Medicine_price'])
            count += 1

        print(str(count)+". Go Back")

        ch = input("Enter medicine ID to add product to cart or go back> ")
        tmp = sp.call('clear', shell=True)

        if(ch==str(count)):
            tmp = sp.call('clear', shell=True)
            customerDashboard(user)
        else:
            addToCart(user, ch)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE> ")
        customerDashboard(user)

def deleteItemFromCart(user, cart_id):

    try:
        query = "SELECT * FROM CART WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        cart = cur.fetchall()
        if(len(cart)==0):
            print("YOU HAVE NO ITEMS IN YOUR CART")
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)


        query = "SELECT * FROM CART WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        rows = cur.fetchall()

        # print(rows)

        print("You have", rows[0]['Items'], "items in your cart.")

        query = "SELECT * FROM CART_ITEM WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        items = cur.fetchall()

        # print(items)
        for item in items:
            query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+item['Medicine_id']+"'"
            cur.execute(query)

            medicine = cur.fetchall()

            print(item['Medicine_id']+".", medicine[0]['Medicine_name'], '-', item['Quantity'],'- Rs.', item['Total_price'])

        id_to_delete = input("Enter item id to delete or enter 999 to go back> ")

        if(id_to_delete==999):
            tmp = sp.call('clear', shell=True)
            customerDashboard(user)

        query = "SELECT * FROM CART_ITEM WHERE Medicine_id='"+id_to_delete+"'"
        cur.execute(query)

        medicine_to_delete = cur.fetchall()

        query = "DELETE FROM CART_ITEM WHERE (Cart_id='"+cart_id+"' AND Medicine_id='"+id_to_delete+"')"
        cur.execute(query)

        query = "UPDATE MEDICINE SET Medicine_stock=Medicine_stock+"+str(medicine_to_delete[0]['Quantity'])+" WHERE Medicine_id='"+id_to_delete+"'"
        cur.execute(query)

        query = "UPDATE CART SET Items=Items-1,"+" Cart_total_price=Cart_total_price-"+str(medicine_to_delete[0]['Total_price'])+" WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)
        con.commit()

        print("Item successfully deleted.")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def checkout(user, cart_id):

    try:
        order_id = uuid.uuid4().hex[:6].upper()

        query = "SELECT * FROM CART WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        rows = cur.fetchall()

        print("You are purchasing the following", rows[0]['Items'], "items:")

        query = "SELECT * FROM CART_ITEM WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        items = cur.fetchall()

        count = 1;
        for item in items:

            query = "INSERT INTO ORDER_ITEM (Order_id, Medicine_id, Quantity, Total_price) VALUES ('"+order_id+"', '"+item['Medicine_id']+"', "+str(item['Quantity'])+", "+str(item['Total_price'])+")"
            cur.execute(query)
            
            query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+item['Medicine_id']+"'"
            cur.execute(query)

            medicine = cur.fetchall()

            print(str(count)+".", medicine[0]['Medicine_name'], '-', item['Quantity'],'- Rs.', item['Total_price'])
            count += 1

        print("Select mode of payment:")
        print("1. NetBanking")
        print("2. COD")
        print("3. UPI")

        ch = int(input("Enter Choice (only input the number)> "))

        mode_of_payment = ""
        if(ch==1):
            mode_of_payment = "NetBanking"
        elif(ch==2):
            mode_of_payment = "COD"
        elif(ch==3):
            mode_of_payment = "UPI"
        else:
            print("No Valid Choice Selected. Defaulting to COD.")
            mode_of_payment = "COD"


        mobile_number = input("Enter Mobile Number> ")
        while(mobile_number.isnumeric()==False):
            print("Please Enter Valid Mobile Number(without country code)")
            mobile_number = input("Enter mobile number> ")
        address_line_1 = input("Enter Address Line 1> ")
        address_line_2 = input("Enter Address Line 2> ")
        city = input("Enter City> ")
        state = input("Enter State> ")
        country = input("Enter Country> ")

        query = "INSERT INTO ORDER_REQUEST (Order_id, Cart_id, Total_price, Items, Mobile_number, Address_line_1, Address_line_2, City, State, Country, Updated_at, Active) VALUES ('"+order_id+"', '"+cart_id+"', "+str(rows[0]['Cart_total_price'])+", "+str(rows[0]['Items'])+", '"+mobile_number+"', '"+address_line_1+"', '"+address_line_2+"', '"+city+"', '"+state+"', '"+country+"', now(), 1)"
        cur.execute(query)

        transaction_id = uuid.uuid4().hex[:6].upper()

        query = "INSERT INTO TRANSACTION (Transaction_id, Order_id, Payment_mode, Completed) VALUES ('"+transaction_id+"', '"+order_id+"', '"+mode_of_payment+"', 1)"
        cur.execute(query)

        query = "UPDATE CART SET Items=0,"+" Cart_total_price=0"+" WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        query = "DELETE FROM CART_ITEM WHERE (Cart_id='"+cart_id+"')"
        cur.execute(query)
        con.commit()

        print("ORDER SUCCESSFULLY PLACED.")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def viewCart(user):

    try:
        cart_id = getCartId(user)
        # print(cart_id)

        if(cart_id=="Invalid"):
            print("You have not added any products to your cart.");
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)

        query = "SELECT * FROM CART WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        rows = cur.fetchall()

        # print(rows)
        if(len(rows)==0):
            print("You have not added any products to your cart.");
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)

        print("You have", rows[0]['Items'], "items in your cart.")

        query = "SELECT * FROM CART_ITEM WHERE Cart_id='"+cart_id+"'"
        cur.execute(query)

        items = cur.fetchall()

        # print(items)
        count = 1;
        for item in items:
            query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+item['Medicine_id']+"'"
            cur.execute(query)

            medicine = cur.fetchall()

            print(str(count)+".", medicine[0]['Medicine_name'], '-', item['Quantity'],'- Rs.', item['Total_price'])
            count += 1


        print(str(count)+". Delete Item") 
        print(str(count+1)+". Proceed to Checkout") 
        print("999. Go Back")

        ch = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if(ch==count):
            deleteItemFromCart(user, cart_id)
        elif(ch==count+1):
            checkout(user, cart_id)
        else:
            customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def addMobile(user):

    try:
        mobile = input("Enter mobile number> ")

        while(mobile.isnumeric()==False):
            print("Please Enter Valid Mobile Number(without country code)")
            mobile = input("Enter mobile number> ")

        query = "INSERT INTO MOBILE_NUMBER (User_id, Mobile_number) VALUES ('"+user['User_id']+"', '"+mobile+"')"

        cur.execute(query)
        con.commit()

        print("MOBILE NUMBER ADDED SUCCESSFULLY")

        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def deleteMobile(user):

    try:
        query = "SELECT * FROM MOBILE_NUMBER WHERE User_id='"+user['User_id']+"'"
        cur.execute(query)

        rows = cur.fetchall()

        if(len(rows)==0):
            print("You don't have any mobile numbers saved.")
            tmp = input("Enter any key to CONTINUE>")
            tmp = sp.call('clear', shell=True)
            customerDashboard(user)
        else:
            print("You have the following Mobile Number(s) saved:")
            count = 1
            for row in rows:
                print(str(count)+".", row['Mobile_number'])
            mobile = input("Enter Mobile Number to Delete: ")

            query = "DELETE FROM MOBILE_NUMBER WHERE Mobile_number='"+mobile+"'"

            cur.execute(query)
            con.commit()

            print("ACTION COMPLETED.")
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def updateMobile(user):

    try:
        query = "SELECT * FROM MOBILE_NUMBER WHERE User_id='"+user['User_id']+"'"
        cur.execute(query)

        rows = cur.fetchall()

        count = 1

        if(len(rows)==0):
            print("You don't have any mobile numbers saved.")
        else:
            print("You have the following Mobile Number(s) saved:")
            for row in rows:
                print(str(count)+".", row['Mobile_number'])

        print(str(count)+". Add Mobile Number")
        print(str(count+1)+". Delete Mobile Number")

        ch = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if(ch==count):
            addMobile(user)
        elif(ch==count+1):
            deleteMobile(user)
        else:
            print("Please Enter a Valid Choice.")
            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)

def customerRegister():

    try:
        query = "SELECT User_id from CUSTOMER ORDER BY length(User_id) DESC, User_id DESC LIMIT 1"
        cur.execute(query)

        rows = cur.fetchall()

        user_id = 1

        if len(rows) == 0:
            user_id = 1
        else:
            last_id = rows[0]['User_id']
            last_id = last_id[2:]
            user_id = int(last_id)+1

        first_name = input("Enter First Name> ")
        last_name = input("Enter Last Name> ")
        email = input("Enter Email Address> ")
        password = input("Enter Password> ")

        query = "INSERT INTO USER (User_id, First_name, Last_name, Email_id, Password) VALUES ('CU"+str(user_id)+"', '"+first_name+"', '"+last_name+"', '"+email+"', MD5('"+password+"'))"
        cur.execute(query)

        # query = "SELECT * FROM USER"
        # cur.execute(query)
        # rows = cur.fetchall()
        # print(rows)

        # input("Enter to continue> ")

        query = "INSERT INTO CUSTOMER (User_id, Cart_id) VALUES ('CU"+str(user_id)+"', 'C"+str(user_id)+"')"
        cur.execute(query)
        con.commit()

        print("USER", first_name, last_name, "ADDED SUCCESSFULLY")
        tmp = input("Enter any key to CONTINUE>")
        landing()
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        landing()

def employeeRegister():

    try:
        query = "SELECT User_id from EMPLOYEE ORDER BY length(User_id) DESC, User_id DESC LIMIT 1"
        cur.execute(query)

        rows = cur.fetchall()

        user_id = 1

        if len(rows) == 0:
            user_id = 1
        else:
            last_id = rows[0]['User_id']
            last_id = last_id[2:]
            user_id = int(last_id)+1

        first_name = input("Enter First Name> ")
        last_name = input("Enter Last Name> ")
        email = input("Enter Email Address> ")
        password = input("Enter Password> ")
        role = input("Enter Role(Admin or Manager)")

        while role != "Admin" and role != "Manager":
            print("Please enter a valid input. ('Admin' or 'Manager')")
            role = input("Enter Role(Admin or Manager)")

        sup_id = ""
        if role == "Manager":
            sup_id = input("Enter SuperVisor ID>")

        query = "INSERT INTO USER (User_id, First_name, Last_name, Email_id, Password) VALUES ('AD"+str(user_id)+"', '"+first_name+"', '"+last_name+"', '"+email+"', MD5('"+password+"'))"
        cur.execute(query)

        query = "INSERT INTO EMPLOYEE (User_id, Role, Supervisor_id) VALUES ('AD"+str(user_id)+"', '"+role+"', '"+sup_id+"')"
        cur.execute(query)
        con.commit()

        print("USER", first_name, last_name, "ADDED SUCCESSFULLY")
        tmp = input("Enter any key to CONTINUE>")
        landing()
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        landing()

def register():

    try:
        print("1. Registering as customer") 
        print("2. Registering as employee")
        ch = int(input("Enter choice> "))
        tmp = sp.call('clear', shell=True)

        if(ch==1):
            customerRegister()
        elif(ch==2):
            employeeRegister()
        else:
            print("Please Enter a valid choice.")
            tmp = input("Enter any key to CONTINUE>")
            landing()
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        landing()

def addMedicine(user):

    try:
        query = "SELECT Medicine_id from MEDICINE ORDER BY length(Medicine_id) DESC, Medicine_id DESC"
        cur.execute(query)

        rows = cur.fetchall()

        medicine_id = 1

        if len(rows) == 0:
            medicine_id = 1
        else:
            last_id = rows[0]['Medicine_id']
            last_id = last_id[1:]
            medicine_id = int(last_id)+1

        medicine_name = input("Enter Medicine Name> ")
        medicine_price = float(input("Enter Medicine Price> "))
        while(isinstance(medicine_price, int)==False and isinstance(medicine_price, float)==False):
                print("Please enter only numeric values.")
                medicine_price = input("Enter Medicine Price> ")
        medicine_description = input("Enter Medicine Description> ")
        manufacturer = input("Enter Medicine Manufacturer> ")
        stock = int(input("Enter Medicine Stock> "))
        while(isinstance(stock, int)==False):
            print("Please enter an integer value.")
            stock = input("Enter Medicine Stock> ")
        expiry = input("Enter Expiry Date (YYYY-MM-DD)> ")

        query = "INSERT INTO MEDICINE (Medicine_id, Medicine_name, Medicine_price, Medicine_description, Manufacturer, Added_at, Added_by, Updated_at, Updated_by, Medicine_stock, Expiry_date) VALUES ('M"+str(medicine_id)+"', '"+medicine_name+"', '"+str(medicine_price)+"', '"+medicine_description+"', '"+manufacturer+"', now(), '"+user['User_id']+"', now(), '"+user['User_id']+"', '"+str(stock)+"', '"+expiry+"')"
        cur.execute(query)

        con.commit()

        print("MEDICINE", medicine_name, "ADDED SUCCESSFULLY")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)
    except Exception as e:
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)


def updateMedicine(user):

    try:
        query = "SELECT * FROM MEDICINE"
        cur.execute(query)

        rows = cur.fetchall()

        print("Following are the medicines in inventory:")

        for row in rows:
            print(row['Medicine_id']+". ", row['Medicine_name'])

        medicine_id = input("Enter Medicine Id to Update> ")

        query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+medicine_id+"'"
        cur.execute(query)

        rows = cur.fetchall()

        print("1. Medicine Name", rows[0]['Medicine_name'])
        print("2. Medicine Price", rows[0]['Medicine_price'])
        print("3. Medicine Description", rows[0]['Medicine_description'])
        print("4. Medicine Manufacturer", rows[0]['Manufacturer'])
        print("5. Medicine Stock", rows[0]['Medicine_stock'])
        print("6. Medicine Expiry Date", rows[0]['Expiry_date'])

        ch = int(input("Enter the number against what you want to edit: "))

        if(ch==1):
            medicine_name = input("Enter Medicine Name> ")
            query = "UPDATE MEDICINE SET Medicine_name='"+medicine_name+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        elif(ch==2):
            medicine_price = float(input("Enter Medicine Price> "))
            while(isinstance(medicine_price, int)==False and isinstance(medicine_price, float)==False):
                print("Please enter only numeric values.")
                medicine_price = input("Enter Medicine Price> ")
            
            query = "UPDATE MEDICINE SET Medicine_price='"+str(medicine_price)+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        elif(ch==3):
            medicine_description = input("Enter Medicine description> ")
            query = "UPDATE MEDICINE SET Medicine_description='"+medicine_description+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        elif(ch==4):
            medicine_manufacturer = input("Enter Medicine manufacturer> ")
            query = "UPDATE MEDICINE SET Manufacturer='"+medicine_manufacturer+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        elif(ch==5):
            medicine_stock = int(input("Enter Medicine Stock> "))
            while(isinstance(medicine_stock, int)==False):
                print("Please enter an integer value.")
                medicine_stock = input("Enter Medicine Stock> ")

            query = "UPDATE MEDICINE SET Medicine_stock='"+str(medicine_stock)+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        elif(ch==6):
            expiry_date = input("Enter Expiry Date(YYYY-MM-DD)> ")
            query = "UPDATE MEDICINE SET Expiry_date='"+expiry_date+"', Updated_by='"+user['User_id']+"', Updated_at=now() WHERE Medicine_id='"+medicine_id+"'"
            cur.execute(query)
            con.commit()
            print("MEDICINE UPDATED")
        else:
            print("PLEASE ENTER A VALID QUERY")

        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)
    except Exception as e:
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)

def updateOrder(user):

    try:
        print("Following are existing orders: ")

        query = "SELECT * FROM ORDER_REQUEST"
        cur.execute(query)

        rows = cur.fetchall()

        for row in rows:
            print(row['Order_id'])

        order_id = input("Enter Order_id to Edit or 999 to go back> ")

        if(order_id==str(999)):
            tmp = sp.call('clear', shell=True)
            employeeDashboard(user)

        query = "SELECT * FROM ORDER_REQUEST WHERE Order_id='"+order_id+"'"
        cur.execute(query)
        rows = cur.fetchall()

        print("Details of order: ")

        print("Order Id:", order_id)
        print("Cart Id:", rows[0]['Cart_id'])
        print("Total Price:", rows[0]['Total_price'])
        print("Number of Items: ", rows[0]['Items'])
        print("Mobile Number: ", rows[0]['Mobile_number'])
        print("Address Line 1: ", rows[0]['Address_line_1'])
        print("Address Line 2: ", rows[0]['Address_line_2'])
        print("City: ", rows[0]['City'])
        print("Sate: ", rows[0]['State'])
        print("Country: ", rows[0]['Country'])
        print("Updated_at: ", rows[0]['Updated_at'])
        print("Updated By: ", rows[0]['Updated_by'])
        print("Active State: ", rows[0]['Active'])

        ch = int(input("Enter 0 or 1 to change Active State (or Enter 999 to Go Back): "))
        if(ch==0):
            query="UPDATE ORDER_REQUEST SET Active=0, Updated_at=now(), Updated_by='"+user['User_id']+"' WHERE Order_id='"+order_id+"'"
            cur.execute(query)
            con.commit()
        elif(ch==1):
            query="UPDATE ORDER_REQUEST SET Active=1, Updated_at=now(), Updated_by='"+user['User_id']+"' WHERE Order_id='"+order_id+"'"
            cur.execute(query)
            con.commit()
        else:
            tmp = sp.call('clear', shell=True)
            updateOrder(user)

        print("ORDER UPDATED.")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)
    except Exception as e:
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)

def updateTransaction(user):

    try:
        print("Following are existing transactions: ")

        query = "SELECT * FROM TRANSACTION"
        cur.execute(query)

        rows = cur.fetchall()

        for row in rows:
            print(row['Transaction_id'])

        transaction_id = input("Enter Transaction_id to Edit or 999 to go back> ")

        if(transaction_id==str(999)):
            tmp = sp.call('clear', shell=True)
            employeeDashboard(user)

        query = "SELECT * FROM TRANSACTION WHERE Transaction_id='"+transaction_id+"'"
        cur.execute(query)
        rows = cur.fetchall()

        print("Details of Transaction: ")

        print("Transaction Id:", transaction_id)
        print("Order Id:", rows[0]['Order_id'])
        print("Payment Mode:", rows[0]['Payment_mode'])
        print("Completed: ", rows[0]['Completed'])

        ch = int(input("Enter 0 or 1 to change Completed State (or Enter 999 to Go Back): "))
        if(ch==0):
            query="UPDATE TRANSACTION SET Completed=0 WHERE Transaction_id='"+transaction_id+"'"
            cur.execute(query)
            con.commit()
        elif(ch==1):
            query="UPDATE TRANSACTION SET Completed=1 WHERE Transaction_id='"+transaction_id+"'"
            cur.execute(query)
            con.commit()
        else:
            tmp = sp.call('clear', shell=True)
            updateTransaction(user)

        print("TRANSACTION UPDATED.")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        employeeDashboard(user)

def removeEmployee(user):

    try:
        query = "SELECT EMPLOYEE.User_id, USER.First_name, USER.Last_Name from EMPLOYEE, USER WHERE EMPLOYEE.Working=1 AND EMPLOYEE.User_id=USER.User_id AND EMPLOYEE.Supervisor_id='"+user['User_id']+"'"
        cur.execute(query)

        rows = cur.fetchall()

        if(len(rows)==0):
            print("No Employees are working under you currently.")
            tmp = int(input("Enter any key to continue> "))
            tmp = sp.call('clear', shell=True)
            employeeDashboard(user)
        else:
            print("Following are the employees working under you:")
            for row in rows:
                print(row['User_id'], "--", row['First_name'], row['Last_Name'])

            emp_id = input("Enter Employee Id to fire or 999 to go back: ")

            if(emp_id==str(999)):
                tmp = sp.call('clear', shell=True)
                employeeDashboard(user)

            confirm = input("You are going to fire "+emp_id+". Are you sure? (Y/N)")

            if(confirm=="Y"):
                query = "UPDATE EMPLOYEE SET Working=0 WHERE User_id='"+emp_id+"'"
                cur.execute(query)
                con.commit()
            else:
                tmp = sp.call('clear', shell=True)
                removeEmployee(user)

        print("EMPLOYEE REMOVED.")
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        employeeDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        con.rollback()
        tmp = input("Enter any key to CONTINUE>")
        employeeDashboard(user)

def viewPrevOrdersCustomer(user):

    try:
        
        last_id = user['User_id']
        last_id = last_id[2:]

        query = "SELECT * FROM ORDER_REQUEST WHERE Cart_id='C"+str(last_id)+"'"
        cur.execute(query)

        rows = cur.fetchall()

        if(len(rows)==0):
            print("You have no previous Orders.")
            tmp = input("Enter any key to CONTINUE>")
            tmp = sp.call('clear', shell=True)
            customerDashboard(user)
        else:
            for row in rows:
                print(row['Order_id'])
            order_id = input("Enter Order id form aove to view details> ")

            query = "SELECT * FROM ORDER_REQUEST WHERE Order_id='"+order_id+"'"
            cur.execute(query)

            rows = cur.fetchall()

            if(len(rows)==0):
                print("Invalid Order Id.")
                tmp = input("Enter any key to CONTINUE>")
                tmp = sp.call('clear', shell=True)
                viewPrevOrdersCustomer(user)
            else:
                print("Details of order: ")
                print("Order Id:", order_id)
                print("Total Price:", rows[0]['Total_price'])
                print("Number of Items: ", rows[0]['Items'])
                print("Mobile Number: ", rows[0]['Mobile_number'])
                print("Address Line 1: ", rows[0]['Address_line_1'])
                print("Address Line 2: ", rows[0]['Address_line_2'])
                print("City: ", rows[0]['City'])
                print("Sate: ", rows[0]['State'])
                print("Country: ", rows[0]['Country'])
                print("Order Placed at: ", rows[0]['Updated_at'])
                print("Items")

                query = "SELECT * FROM ORDER_ITEM WHERE Order_id='"+order_id+"'"
                cur.execute(query)

                rows = cur.fetchall()

                count = 1
                for row in rows:
                    query = "SELECT * FROM MEDICINE WHERE Medicine_id='"+row['Medicine_id']+"'"
                    cur.execute(query)

                    medicine = cur.fetchall()

                    print(str(count)+". "+medicine[0]['Medicine_name']+" -- "+str(row['Quantity'])+" -- "+str(row['Total_price']))
                    count += 1

                tmp = input("Enter any key to CONTINUE>")
                tmp = sp.call('clear', shell=True)
                customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        customerDashboard(user)



def dispatch(ch, user=None):

    try:
        if(ch == 1):
            login()
        elif(ch == 2):
            register()
        elif(ch == 3):
            viewPrevOrdersCustomer(user)
        elif(ch == 4):
            browseProducts(user)
        elif(ch == 5):
            viewCart(user)
        elif(ch == 6):
            updateMobile(user)
        elif(ch==7):
            tmp = sp.call('clear', shell=True)
            landing()
        elif(ch == 8):
            addMedicine(user)
        elif(ch == 9):
            updateMedicine(user)
        elif(ch == 10):
            updateOrder(user)
        elif(ch == 11):
            removeEmployee(user)
        elif(ch == 12):
            updateTransaction(user)
        else:
            print("Error: Invalid Option")
    except Exception as e:
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        tmp = sp.call('clear', shell=True)
        landing()

def employeeDashboard(user):

    try:
        print("Welcome,", user['First_name'], user['Last_name'], ". You are logged in.")
        print("Your employer ID is:", user['User_id'])

        query = "SELECT * FROM EMPLOYEE WHERE User_id='"+user['User_id']+"'"
        cur.execute(query)

        rows = cur.fetchall()

        ch = 13

        if(rows[0]['Role']=="Admin"):
            print("8. Add to Medicine Inventory")
            print("9. Update Medicine Inventory")
            print("10. Update Order")
            print("11. Remove Employee")
            print("12. Update Transaction")
            print("7. Logout")
            ch = int(input("Enter choice> "))
            while(ch<7):
                ch = int(input("Enter valid choice> "))
            tmp = sp.call('clear', shell=True)
            dispatch(ch, user)
            employeeDashboard(user)
        else:
            print("8. Add to Medicine Inventory")
            print("9. Update Medicine Inventory")
            print("7. Logout")
            ch = int(input("Enter choice> "))
            while(ch<7):
                ch = int(input("Enter valid choice> "))
            while(ch>9 and ch<13):
                ch = int(input("Enter valid choice> "))
            tmp = sp.call('clear', shell=True)
            dispatch(ch, user)
            employeeDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        landing()

def customerDashboard(user):
    try:
        print("Welcome,", user['First_name'], user['Last_name'], ". You are logged in.")
        while(1):
            tmp = sp.call('clear', shell=True)
            print("3. View Previous Orders") 
            print("4. Browse Products") 
            print("5. View Cart") 
            print("6. Update Mobile Number")
            print("7. Logout")
            ch = int(input("Enter choice> "))
            while(ch<3):
                ch = int(input("Enter Valid choice> "))
            while(ch>7):
                ch = int(input("Enter Valid choice> "))
            tmp = sp.call('clear', shell=True)
            dispatch(ch, user)

            tmp = input("Enter any key to CONTINUE>")
            customerDashboard(user)
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        landing()

def login():

    try:
        username = input("Enter Email Id: ")
        password = input("Enter Password: ")

        tmp = sp.call('clear', shell=True)

        query = "SELECT * FROM USER WHERE Email_id='" + username + "' AND Password=MD5('" + password + "')"
        cur.execute(query)

        rows = cur.fetchall()

        if(len(rows)==1):
            user_id = rows[0]['User_id']
            if(user_id[0:2]=="AD"):
                query = "SELECT * FROM EMPLOYEE WHERE User_id='"+user_id+"' AND Working=1"
                cur.execute(query)

                employees = cur.fetchall()
                if(len(employees)==1):
                    employeeDashboard(rows[0])
                else:
                    print("Invalid Credentials.")
                    tmp = input("Enter any key to CONTINUE>")
                    landing()
            else:
                customerDashboard(rows[0])

        else:
            print("Invalid Credentials.")
            tmp = input("Enter any key to CONTINUE>")
            landing()
    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")
        landing()

def landing():
    tmp = sp.call('clear', shell=True)
    print("1. Login") 
    print("2. Register")
    ch = int(input("Enter choice> "))
    tmp = sp.call('clear', shell=True)
    dispatch(ch)
    tmp = input("Enter any key to CONTINUE>")
    landing()

while(1):
    tmp = sp.call('clear', shell=True)

    print("Enter username and password to access the database.")
    
    username = input("Username: ")
    password = input("Password: ")

    try:
        con = pymysql.connect(host='localhost',
                              user=username,
                              password=password,
                              db='MYMEDICINE',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)


        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        cur = con.cursor()
        print(cur)
        
        landing()

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        tmp = input("Enter any key to CONTINUE>")