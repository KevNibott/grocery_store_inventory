from models import (Base, session, Brand, Product, engine)
from datetime import date
import datetime
import time
import csv
import sys


def setup():
    looper = 0
    while True:
        if looper != 0:
            time.sleep(1.5)
            introduction_2()
        else:
            introduction_1()
            pass
        looper += 1
        choice = input(" > ")    
        if choice.lower() == "v":
            v()
        elif choice.lower() == "n":
            n()
        elif choice.lower() == "a":
            a()
        elif choice.lower() == "b":
            b()
        elif choice.lower() == "f":
            exit()
        else:
            print("Wrong key, try again.")
            if looper > 3:
                fatal_error()
            continue

def v():
    loop = 0
    while True:
        total_number_of_products = session.query(Product).filter(Product.product_id).count()
        if loop == 0:
            choice = input(f"\nEnter an ID number (from 1 to {total_number_of_products}) or a non-digit key to go back to main menu:\n > ")
        else:
            choice = input(f"\nAre you here again? Ok, enter another valid Product ID number (from 1 to {total_number_of_products}) or any other key to go back to main menu:\n > ")
        try:
            int(choice)
            pass
        except Exception:
            print("\nSee you!")
            break
        if int(choice) > total_number_of_products:
            print("\nNot a valid answer! See you!")
            break
        else:
            for product_info in session.query(Product).filter_by(product_id=choice):
                id_to_obtain_brand = product_info.brand_id
                for brand in session.query(Brand).filter_by(brand_id=id_to_obtain_brand):
                    name_of_the_brand = brand.brand_name
                print(f"\nProduct: {product_info.product_name}\nBrand: {name_of_the_brand}\nAmount: {product_info.product_quantity}\nPrice per unit: {product_info.product_price/100}$")
        time.sleep(1.5)
        if loop == 0:
            print("\nAmazing information, right? What do you want to do with it now?")
        else:
            print("\nAnother bunch of almighty information. What do you want to do with it now?")
        while True:
            looper = 0
            print("""
        * Press 'E' to Edit the entry 
        * Press 'D' to Delete the entry 
        * Press 'K' to Keep viewing information of any other product
        """)
            answer = input(" > ")    
            if answer.lower() == "e":
                lolooper = 0
                while True:
                    possible_answer = ["n","b","p","q"]
                    if lolooper == 0:
                        print("\nWhat field do you want to change?")
                    else:
                        print("\nWhat else do you want to change?")
                    print("""
        * Press 'N' for Product Name
        * Press 'B' for Brand ID
        * Press 'P' for Price
        * Press 'Q' for Quantity
        * Press 'F' to stop the editing
        """) 
                    editing_answer = input(" > ")
                    if editing_answer.lower() == "f":
                        break
                    elif editing_answer.lower() in possible_answer:
                        editing_after_viewing(editing_answer,product_info)
                        lolooper +=1
                        continue
                    else:
                        fatal_error()
            elif answer.lower() == "d":
                re_answer = input("\nAre you sure? Press 'Y' for Yes, or any other key for No\n > ")
                if re_answer.lower() == "y":
                    re_re_answer = input("\nAre you sure, sure? Remember: 'Y' for Yes or press ANY OTHER KEY to stop this madness\n > ")
                    if re_re_answer.lower() == "y":
                        print("\nRude! Ok then...")
                        loading_bar()
                        session.delete(product_info)
                        session.commit()
                        print("\nSad. Now it's gone... forever!!!")
                    else:
                        print("\nPiuuuf! That was close...")
                        break
                else:
                    print("\nHa! Nice choice...")
                    break
                break
            elif answer.lower() == "k":
                break
            elif answer.lower() == "f":
                exit()
            else:
                print("\nSorry, that's not a valid answer. Try again")
                if looper > 2:
                    fatal_error()
                looper += 1 
                continue
        loop += 1

def n():
    print("\nExciting! We are going to add a new product to the database!")
    while True:
        looper = 0
        time.sleep(2)
        name = input("\nPlease, enter the name or a brief description of the product:\n > ")
        time.sleep(1)
        for item_name in session.query(Product).filter(Product.product_name==name):
            name_to_check = item_name.product_name
        try:
            if name == name_to_check:
                print("\nIt seems that this item is already in the database, so instead of adding a new one, we are editing the existing one, ok? Let's continue...")
            looper += 1
        except Exception:
            pass
        quantity = input("\nWe also need to know the quantity:\n > ")
        try:
            int(quantity)
        except Exception:
            fatal_error()
        time.sleep(1)
        try:
            price = float(input("\nHow much is going to cost per unit in dollars (enter only digits eg. '2.35'):\n > "))*100
        except Exception:
            fatal_error()
        today = date.today()
        time.sleep(1)
        print("\nNow, we are going to show you a list of brands and its ID number. Select the ID you want to associate with the product you are adding/editing:\n")
        time.sleep(0.3)
        while True:
            for brand in session.query(Brand):
                print(f"{brand.brand_name}, and its ID: {brand.brand_id}")
                time.sleep(0.3)
            id = input("\nEnter the ID number:\n > ")
            try:
                int(id)
                time.sleep(0.8)
            except Exception:
                fatal_error()
            if int(id) > 13:
                print("\nThat's not a valid ID, try again.\n > ")
                time.sleep(2)
                continue
            elif int(id) < 1:
                print("\nThat's not a valid ID, try again.\n > ")
                time.sleep(2)
                continue
            else:
                break
        today = date.today()
        new_entry = Product(
            product_name=name, product_quantity=int(quantity), product_price=int(price), date_updated=today, brand_id=int(id)
        )
        print("\nSo, this is the new entry summary:\n")
        time.sleep(0.8)
        print(f"""
        * The product name: {name}
        * Quantity storaged: {quantity} units
        * Price per unit: {price/100}$
        * And last but not least, the brand ID: {id}
        """)
        time.sleep(0.8)
        answer = input("\nIs everything correct? Yes or No?\nPress 'Y' to complete the new adding to the database\nPress 'N' to start over\nPress 'F' to cancel and go back to the main menu.\n > ")
        if answer.lower() == "y":
            if looper > 0:
                item_name.product_quantity = int(quantity)
                item_name.product_price = int(price)
                item_name.date_updated = today
                item_name.brand_id = int(id)
            else:
                session.add(new_entry)
            session.commit()
            time.sleep(2)
            print("And...")
            loading_bar()
            print("Done! The new entry has been added correctly\n")
            break
        elif answer.lower() == "n":
            continue
        else:
            print("\nSee you!")
            break

def a():
    print("\nOk, let's recapitulate:")
    time.sleep(0.8)
    for cheap_item in session.query(Product.product_price).order_by(Product.product_price).first():
        for product in session.query(Product).filter(Product.product_price==cheap_item):
            cheap_product = product.product_name
    for expensive_item in session.query(Product.product_price).order_by(Product.product_price.desc()).first():
        for product in session.query(Product).filter(Product.product_price==expensive_item):
            expensive_product = product.product_name
            expensive_product_id = product.brand_id
            for brands in session.query(Brand).filter(Brand.brand_id==expensive_product_id):
                brand_of_the_expensive_product = brands.brand_name
    number_of_brands = session.query(Brand).count()
    dictionary_of_brands_and_count = {}
    for number in range(number_of_brands):
        count_brand = session.query(Product).filter(Product.brand_id == number).count()
        for item in session.query(Brand).filter(Brand.brand_id == number):
            name = item.brand_name
            dictionary_of_brands_and_count[name]=count_brand
    number_max_of_brands = max(dictionary_of_brands_and_count.values())
    key_brand = [key for key,value in dictionary_of_brands_and_count.items() if value == number_max_of_brands]
    dictionary_of_quantity_count = {}
    for item in session.query(Product).order_by(Product.product_id):
        name = item.product_name
        dictionary_of_quantity_count[name]=item.product_quantity
    number_max_of_quantity = max(dictionary_of_quantity_count.values())
    key_product = [key for key,value in dictionary_of_quantity_count.items() if value == number_max_of_quantity]
    for olaf_item in session.query(Product).filter(Product.product_id==20):
        olaf_favorite_product = olaf_item.product_name
        olaf_favorite_product_price = olaf_item.product_price
    loading_bar()
    print(f"""
        * Least expensive item of the database: '{cheap_product}', and it costs {cheap_item/100}$
        * Most expensive item of the database: '{expensive_product}', and it costs {expensive_item/100}$
        * Brand of our '{expensive_product}': {brand_of_the_expensive_product}
        * Most repeated brand along the database: {key_brand[0]}, with a total of {number_max_of_brands} different items
        * The product with the largest quantity in storage: '{key_product[0]}', with a total of {number_max_of_quantity} units storaged
        * And the most valuable data, the Olaf's favorite item: '{olaf_favorite_product}', and it costs only {olaf_favorite_product_price/100}$, our boss is so humble...
        """)
    time.sleep(8)

def b():
    current_time = datetime.datetime.now()
    print(f"\nCreating the backup .csv file at current time: {current_time}...")
    loading_bar()
    with open("brand_backup_file.csv","w",newline="") as file_open: 
        brand_table_backup = csv.writer(file_open)
        list_of_rows = []
        header = ["Brand ID","Brand Name"]
        brand_table_backup.writerow(header)
        for item in session.query(Brand):
            row = [item.brand_id, item.brand_name]
            list_of_rows.append(row)
        for line in list_of_rows:
            brand_table_backup.writerow(line)
    with open("product_backup_file.csv","w",newline="") as file_open: 
        product_table_backup = csv.writer(file_open)
        list_of_rows = []
        header = ["Product ID","Product Name","Product Quantity","Product Price($)","Last Update(mm/dd/yyyy)","Brand Name"]
        product_table_backup.writerow(header)
        for item in session.query(Product):
            csv_date = datetime.datetime.strptime(str(item.date_updated), "%Y-%m-%d").strftime("%m/%d/%Y")
            for item_brand in session.query(Brand).filter(Brand.brand_id==item.brand_id):
                csv_brand = item_brand.brand_name
            row = [item.product_id, item.product_name,item.product_quantity,"$"+str(item.product_price/100),csv_date,csv_brand]
            list_of_rows.append(row)
        for line in list_of_rows:
            product_table_backup.writerow(line)
    time.sleep(2)
    print("\nDone!")

def loading_bar():
    bar = "........\n"
    for item in bar:
        sys.stdout.write(item)
        sys.stdout.flush()
        time.sleep(0.4)

def introduction_1():
    print("""\nWelcome to Olaf the Fat Cat Store's inventory database.\nFollow the instructions to navigate through the database:\n
        - Press 'V' to view details of a single product.\n
        - Press 'N' to add a new product to the database.\n
        - Press 'A' to view an analysis.\n
        - Press 'B' to make a database backup.\n
        - Press 'F' to exit.\n""")

def introduction_2():
    print("""\nWelcome back to the amazing main menu of Olaf the Fat Cat Store's inventory database...\nFollow the instructions to navigate through the database:\n
        - Press 'V' to view details of a single product.\n
        - Press 'N' to add a new product to the database.\n
        - Press 'A' to view an analysis.\n
        - Press 'B' to make a database backup.\n
        - Press 'F' to exit.\n""")

def editing_after_viewing(answer,product):
    today = date.today()
    if answer.lower() == "n":
        new_name = input("\nGive me a better name... if you can\n > ")
        product.product_name = new_name
        product.date_updated = today
        loading_bar()
        session.commit()
        print("\nDone!")
    elif answer.lower() == "b":
        number_of_brand_id = session.query(Brand).count()
        new_brand_id = input(f"\nChanging Brand ID it is! It has to be a number from 1 to {number_of_brand_id}\n > ")
        try:
            if int(new_brand_id) <= 13:
                product.product_brand_id = int(new_brand_id)
                product.date_updated = today
                loading_bar()
                session.commit()
                print("\nDone!")
            else:
                print("\nWrong!")
                fatal_error()
        except Exception:
            print("\nWrong!")
            fatal_error()
    elif answer.lower() == "p":
        new_price = input("\nYeah! I don't like that price either. The new price has to be in dollars and only digits (eg. '8.97')\n > ")
        try:
            new_price_in_cents = float(new_price)*100
            product.product_price = new_price_in_cents
            product.date_updated = today
            loading_bar()
            session.commit()
            print("\nDone!")
        except Exception:
            print("\nWrong!")
            fatal_error()
    elif answer.lower() == "q":
        new_quantity = input("\nOh wait! What happen? Do we have more... or do we have less??? Enter the new quantity and remember, digits only!\n > ")
        try:
            new_quantity_verified = int(new_quantity)
            product.product_quantity = new_quantity_verified
            product.date_updated = today
            loading_bar()
            session.commit()
            print("\nDone!")
        except Exception:
            print("\nWrong!")
            fatal_error()

def fatal_error():
    print("\nHEY! That's not a correct answer and Olaf is a really busy cat, don't waste our time!\n")
    exit()

def cleaning_date(str_to_trasnform_to_date_type):
    list_of_date_str_data = str_to_trasnform_to_date_type.split("/")
    year = int(list_of_date_str_data[2])
    month = int(list_of_date_str_data[0])
    day = int(list_of_date_str_data[1])
    return datetime.date(year,month,day)

def fill_brand_table():
    if session.query(Brand).filter_by(brand_id=1).first() is not None:
        pass
    else:
        with open ("brands.csv", "r") as inventory_file:
            filter_added = (row.replace("\n", "") for row in inventory_file) #To delete the "\n" at the end of each row
            list_of_rows = []
            for row in csv.reader(filter_added):
                list_of_rows.append(row[0])
            for text in list_of_rows[1:]:
                adding_new_text = Brand(brand_name = text)
                session.add(adding_new_text)
        session.commit()

def fill_product_table():
    if session.query(Product).filter_by(product_id=1).first() is not None:
        pass
    else:
        with open ("inventory.csv", "r") as inventory_file: 
            filter_added = (row.replace("\n", "") for row in inventory_file) #To delete the "\n" at the end of each row
            list_of_rows = []
            for row in csv.reader(filter_added):
                list_of_rows.append(row)
            for item in list_of_rows[1:]:
                price_in_cents = float(item[1][1:])*100 #Transform the product_price to cents
                brand_to_obtain_id = item[4]
                for brand in session.query(Brand).filter_by(brand_name=brand_to_obtain_id):
                    id_number = brand.brand_id
                new_product = Product(
                    product_name = item[0], product_quantity = int(item[2]), 
                    product_price = int(price_in_cents), date_updated = cleaning_date(item[3]),
                    brand_id = id_number
                )
                session.add(new_product)
        session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    fill_brand_table()
    fill_product_table()
    setup()