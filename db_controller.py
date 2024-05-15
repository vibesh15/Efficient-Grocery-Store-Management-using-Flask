from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import BuyLog, Category, Manager, Product, User, Cart
from database.configdb import create_engine
from database.configdb import engine
from datetime import datetime
import re 


def loginAdmin(managername, password):
    print("Checking Manager Auth...")
    with Session(engine) as session:
        manager = session.query(Manager).filter_by(managername=managername).first()
        if manager is None:
            print("Manager not found!")
            return None
        if manager.password == password:
            print("Manager Authenticated!")
            return manager
        else:
            print("Manager not authenticated! Wrong password!")
            return None


def createNewCategory(categoryName):
    print("Creating new category...")
    with Session(engine) as session:
        try:
            category = session.query(Category).filter_by(name=categoryName).first()
            if(category == None):
                category = Category(name=categoryName)
                session.add(category)
                session.commit()
                return category
            else:
                return "Already Exists"
        except Exception as e:
            print("Some error occured while creating category", e)
            session.rollback()
            return None
        

def deleteCateogry(id):
    print("Deleting category...")

    if(deleteAllPrductsByCategoryId(id)):
        with Session(engine) as session:
            try:
                category = session.query(Category).filter_by(id=id).first()
                if category is None:
                    print("Category not found!")
                    return None
                session.delete(category)
                session.commit()
                print("Category deleted:", category.name)
                return category
            except Exception as e:
                print("Some error occured while deleting category", e)
                session.rollback()
                return None
            

def editCategory(id , name):
    print("Editing category with id:", id)

    
    with Session(engine) as session:
        try:
            category = session.query(Category).filter_by(id=id).first()
            if category is None:
                print("Category not found!")
                return "Category not found!"
            category.name = name
            session.commit()
            print("Category Edited:", category.name)
            return category
        except Exception as e:
            print("Some error occured while Editing category", e)
            session.rollback()
            return "Some error occured"


def getAllCategories():
    print("Getting all categories...")
    try:
        with Session(engine) as session:
            categories = session.query(Category).all()
            print("All categories fetched!")
            return categories
    except Exception as e:
        print("Some error occured while fetching categories", e)
        session.rollback()
        return None
    
def addNewProductDB(
        prdName , 
        category , 
        price, 
        quantity , 
        unit,  
        manufactureDate, 
        expiryDate
    ):
    print("Adding new Product in DB...")
    try:
        with Session(engine) as session:
            prod = session.query(Product).filter_by( name = prdName ,category_id=category).first()
            prod= None
            if(prod == None):
                prod = Product(
                    name= prdName , 
                    category_id = category , 
                    unit = unit , 
                    quantity = quantity , 
                    price = price,
                    manufacture_date = manufactureDate,
                    expiry_date = expiryDate,
                )
                session.add(prod)
                session.commit()
                print("New Product Created:" , prod.name)
                return prod
            else:
                print("Product Already Exists!")
                return "Already Exists"
    except Exception as e:
        print("Error while addin prod in db" , e)
        return "Internal Server Error"


def getProductsWithCategoryId(id):
    print("Fetching product with product Id:", id)
    try:
        with Session(engine) as session:
            prods = session.query(Product).filter_by(category_id = id).all()
            print("Success: Fetching product with product Id:", id)
            if(len(prods) == 0):
                return []
            else:
                return prods
    except Exception as e:
        print("Some Error Occured While fetching products form Product Id:",e)
        return []

def deleteAllPrductsByCategoryId(id):
    print("Deleting all products with category Id:", id)
    try:
        with Session(engine) as session:
            prods = session.query(Product).filter_by(category_id = id).all()
            if(len(prods) == 0):
                return True
            else:
                for prod in prods:
                    session.delete(prod)
                print("All Products Deleted with catrgoty id:",id)
                session.commit()
                return True
    except Exception as e:
        print("Some Error Occured While deleting products all form Catrgory Id:",e)
        return False
    
def editPrductWithProductId(
        id , 
        productName, 
        unit, 
        price, 
        quantity,
        manufactureDate,
        expiryDate
    ):
    print("Product Editing in db with prodcut id:" ,id)
    with Session(engine) as session:
        try:
            product = session.query(Product).filter_by(id = id).first()
            if(product == None):
                print("Product not found while editing product id")
                return "Product not Found"
            else:
                print("Product found while editing product id")
                product.name = productName
                product.unit = unit
                product.price = price
                product.quantity = quantity
                product.manufacture_date = manufactureDate
                product.expiry_date = expiryDate
                session.commit()
                print("Succes editing product in db")
                return product
        except Exception as e:
            print("Some error occured while ediitng product:", e)
            session.rollback()
            return "Some Error Ocucred"
    
def deletePrductWithProductId(id ):
    print("Product Deleting in db with prodcut id:" ,id)
    
    with Session(engine) as session:
        try:
            product = session.query(Product).filter_by(id = id).first()
            if(product == None):
                print("Product not found while editing product id")
                return False
            else:
                print("Product found while editing product id",  id)
                session.delete(product)
                session.commit()
                return True
        except Exception as e:
            print(e)
            session.rollback()
            return False


#----------User Routes Starts here-------------#


def createUserDB(username , password , address, phone ):
    print("Creating New User...")
    with Session(engine) as session:
        try:
            user = session.query(User).filter_by(username = username).first()
            if(not user == None):
                print("Username already exists")
                return "Username Already Exists!"
            user = User(
                username = username, 
                address = address, 
                phone = phone, 
                password = password
            )
            session.add(user)
            session.commit()
            print("User created.")
            return user
        except Exception as e:
            print("Some Error occured while creating user!: ", e)
            session.rollback()
            return "Some Error Occured"


def authUserDB(username , password):
    print("User Auth started...")
    with Session(engine) as session:
        try:
            user = session.query(User).filter_by(username = username).first()
            if(user == None):
                print("Username not found")
                return "Username Not Found!"
            else:
                if(user.password == password):
                    print("User Authenticated")
                    return user
                else:
                    print("Password Incorrect")
                    return "Password Incorrect!"
        except Exception as e:
            print("Some Error occured while authenticating user!: ", e)
            return "Internal Server Error!"


def AddProductToCartDB(userId , productId , productName, quantity):
    print("ADD product to cart DB functon...")
    with Session(engine) as session:
        try:
            cartEntry = session.query(Cart).filter_by(
                product_id = productId , 
                user_id = userId
            ).first()
            product = session.query(Product).filter_by(id = productId).first()
            if(cartEntry is None):
                cartEntry = Cart(
                    user_id = int(userId), 
                    product_id = int(productId), 
                    product_name = productName, 
                    quantity = int(quantity),
                )
                product.quantity -= quantity
                session.add(cartEntry)
                session.merge(product)
                newquantity = cartEntry.quantity
                session.commit()
                print(quantity , productName , "Added to Cart")
                return cartEntry, newquantity
            else:
                cartEntry.quantity += quantity
                product.quantity -= quantity
                session.merge(cartEntry)
                session.merge(product)
                newquantity = cartEntry.quantity
                session.commit()
                print("Cart Entry Updated")
                return cartEntry , newquantity
        except Exception as e:
            session.rollback()
            print("Some Error occured while Adding item to cart!: ", e)
            return "Internal Server Error!" ,0
        
def deleteItemFromCartDB(id):
    print("Deleting Item form cart with cart entry number: " , id)
    with Session(engine) as session:
        try:
            cartEntry = session.query(Cart).filter_by(id=id).first()
            
            if cartEntry is None:
                print("Cart entry not found")
                return "Item not found in the cart"
            else:
                product = session.query(Product).filter_by(id = cartEntry.product_id).first()
                product.quantity += cartEntry.quantity
                print("Deleted item form cart")
                session.delete(cartEntry)
                session.commit()
                return cartEntry
        except Exception as e:
            session.rollback()
            print("Some error occured while delting item form cart: ", e)
            return "Internal Server Error"

def getCartEntryDB(userId, productId):
    with Session(engine) as session:
        try:
            cartEntry = session.query(Cart).filter_by(
                user_id = userId, 
                product_id = productId
            ).first()
            if not cartEntry is None:
                return cartEntry
            else:
                return None 
        except Exception as e:
            print("Some error occured while fetching cart entry: ", e)
            return None


def getProdcutByProductId(id):
    with Session(engine) as session:
        try:
            product = session.query(Product).filter_by(id=id).first()
            
            if(product is None):
                return None
            else:
                print("Product found: ",product.quantity)
                return product

        except Exception as e:
            print("Some Error occured while fetching product iwth product id: " , e)
            return "Internal Server Error" 
        
def getUserCartFromUserIdDB(userId):
    print("getUserCartFromUserIdDB funciton call... ")
    with Session(engine) as session:
        try:
            cart = session.query(Cart).filter_by(user_id = userId).all()
            return cart 
        except Exception as e:
            print("Some Error occured while fetching cart of user!",e)
            return []
                

def deleteAllItemFromCartForAUser(userId):
    with Session(engine) as session:
        try: 
            cartEntries = session.query(Cart).filter_by(user_id = userId).all()
            if(not cartEntries is None):
                for entry in cartEntries:
                    session.delete(entry)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Some Error occured while deleting all cart entries for a user!",e)
            session.rollback()
            return False
        
def buyOneProductDB(userId , productId, productQuantity):
    print("buyOneProductDB function call...")
    with Session(engine) as session:
        try:
            product = session.query(Product).filter_by(id = productId).first()
            if( product is None):
                return "Product Not Found!"
            else:
                if(int(productQuantity) <= product.quantity):
                    product.quantity -= int(productQuantity)
                    category = session.query(Category).filter_by(id = product.category_id).first()
                    date = str(datetime.now().date())
                    time = str(datetime.now().strftime('%H:%M'))
                    print("Time: ", time)
                    log = BuyLog(
                        user_id = userId,
                        product_id = productId,
                        product_name = product.name,
                        category_name = category.name,
                        category_id = product.category_id,
                        quantity = int(productQuantity),
                        date = date,
                        time = time
                    )
                    session.add(log)
                session.commit()
                return True
        except Exception as e:
            print("Internal Server Error!", e)
            session.rollback()
            return "Internal Server Error!"

def buyAllFromCartDB(userId):
    print("buyAllFromCartDB function call...")
    with Session(engine) as session:
        try:
            cartEntries = session.query(Cart).filter_by(user_id = userId).all()
            if(not cartEntries is None):
                for entry in cartEntries:
                    product = session.query(Product).filter_by(id = entry.product_id).first()
                    category = session.query(Category).filter_by(id = product.category_id).first()
                    date = str(datetime.now().date())
                    time = str(datetime.now().strftime('%H:%M'))
                    log = BuyLog(
                        user_id = userId, 
                        product_id = entry.product_id, 
                        product_name = entry.product_name, 
                        category_name = category.name,
                        category_id = category.id,
                        quantity = entry.quantity,
                        time =  time,
                        date = date,
                    )
                    session.add(log)
                    session.delete(entry)
                session.commit()
                return True
            else:
                return "Cart is Empty!"
        except Exception as e:
            session.rollback()
            print("Internal Server Error" ,e)
            return "Internal Server Error"
        
def getAllLogs():
    print("getAllLogs function call...")
    with Session(engine) as session:
        try:
            logs = session.query(BuyLog).all()
            return logs
        except Exception as e:
            print("Internal Server Error!", e)
            return "Internal Server Error!"
        

def editProfileDB(user , newUsername ,newPassword ,newAddress,newPhone):
    print("Editing profile in db...")
    with Session(engine) as session:
        try:
            copyUser = session.query(User).filter_by(username=newUsername).first()
            newUser = session.query(User).filter_by(id=user.id).first()
            if(not copyUser is None and not copyUser.id == newUser.id ):
                return f"Username '{newUsername}' is already taken by someone else"
            if(newUser is None):
                print("User not found")
                return "User not found!"
            else:
                newUser.username = newUsername
                newUser.address = newAddress
                newUser.phone = newPhone
                newUser.password = newPassword
                session.commit()
                print("User updated susscessfully")
                nu = session.query(User).filter_by(id = newUser.id).first()
                return nu 
        except Exception as e:
            print("Some error occured while editing profile!: ", e)
            session.rollback()
            return "Internal Server Error"


def getLogsWithUserId(id):
    with Session(engine) as session:
        try:
            logs = session.query(BuyLog).filter_by(user_id=id).all()
            if logs is None:
                return []
            else:
                print(logs)
                return logs
        except:
            return []
        
def searchItemDB(key):
    with Session(engine) as session:
        try:
            prods = session.query(Product).all()
            categoies = session.query(Category).all() 
            matchedProds = []
            matchedCat = []
            for prod in prods:
                if(re.match(key.upper() , prod.name.upper())):
                    matchedProds.append(prod)
            for cat in categoies:
                if(re.match(key.upper() ,cat.name.upper())):
                    matchedCat.append(cat)
            return matchedProds , matchedCat
        except Exception as e:
            return [], []