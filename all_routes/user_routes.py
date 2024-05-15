from flask import render_template,redirect
from database.configdb import *
from database.db_controller import *

from flask import request
from flask import current_app as app

 
@app.route("/" , methods =["POST"])
def UserDashboardRoute():
    print(request.form)
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    user = authUserDB(username , password)
    if(request.form["action"] == "ADDTOCART" and not isinstance(user , str)):
        return addToCart(request)
    if isinstance(user , str):
        return render_template(
            "user_screens/login_screen.html", 
            error=user 
        )
    else: 
        categories = getAllCategories()
        products = {}
        for category in categories:
            tempProds = getProductsWithCategoryId(category.id)
            products[category.id] = tempProds
        return render_template(
            "user_screens/user_dashboard.html", 
            username = user.username,
            password = user.password, 
            userId = user.id,
            categories=categories,
            products = products, 
        )
@app.route("/auth" , methods =["GET"])
def UserLoginGetRoute():
    return render_template("user_screens/login_screen.html" )


@app.route("/auth" , methods =["POST"])
def UserLoginPostRoute():
    try:
        if(request.form["action"] == "CREATEACCOUNT"):
            return createUserAccount(request)
    except Exception as e:
        pass
    return render_template("user_screens/login_screen.html" )

def createUserAccount(request):
    print("Create user Account request...")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    address = request.form["address"]
    phone = request.form["phone"]
    user = createUserDB(
            username = username,
            password = password,
            address = address,
            phone = phone 
        )
    if(user == "Username Already Exists!" or user == "Some Error Occured"):
        return render_template(
            "user_screens/signup_screen.html", 
            error=user 
        )
    return render_template(
        "user_screens/login_screen.html", 
        success = "User Created Successfully" 
    )

@app.route("/signup" , methods =["GET", "POST"])
def UserSignupRoute():
    return render_template("user_screens/signup_screen.html" )

@app.route("/addtocart" , methods =["GET"])
def BuyProductGetRoute():
    return redirect("/")

@app.route("/addtocart" , methods =["POST"])
def BuyProductPostRoute():
    print("Buy Product Request...")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username , password)
    productId = request.form["productId"]
    productName = request.form["productName"]
    unit = request.form["unit"] 
    price = request.form["price"]
    quantity = request.form["quantity"]
    productId = request.form["productId"]
    manufactureDate = request.form["manufactureDate"]
    expiryDate = request.form["expiryDate"]
    # cartEntry = getCartEntryDB(userId= user.id , productId=productId)
    if isinstance(user , str):
        return redirect("/" )

    return render_template(
        "user_screens/add_to_cart.html", 
        username=user.username, 
        password = user.password, 
        userId = user.id,
        productName =productName,
        unit =unit, 
        price =price, 
        quantity =quantity, 
        productId = productId,
        manufactureDate = manufactureDate,
        expiryDate = expiryDate,
    )

def addToCart(request):
    username = request.form["username"]
    password = request.form["password"]
    productName = request.form["productName"]
    unit = request.form["unit"]
    price = request.form["price"]
    cartQuantity = request.form["cartQuantity"]
    productId = request.form["productId"]
    manufactureDate = request.form["manufactureDate"]
    expiryDate = request.form["expiryDate"]
    user = authUserDB(username=username , password= password)
    cartEntry, newCartQuantity = AddProductToCartDB(
        productId= int(productId),
        userId= user.id,
        productName=productName,
        quantity= int(cartQuantity)
    )
    product = getProdcutByProductId(id=productId)
    if( isinstance(cartEntry , str)):
        return render_template(
            "user_screens/add_to_cart.html", 
            username=user.username, 
            password = user.password, 
            userId = user.id,
            productName =productName,
            unit =unit, 
            price =price, 
            quantity =product.quantity, 
            productId = productId,
            error = cartEntry,
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
        )
    else:
        return render_template(
            "user_screens/add_to_cart.html", 
            username=user.username, 
            password = user.password, 
            userId = user.id,
            productName =productName,
            unit =unit, 
            price =price, 
            quantity =product.quantity, 
            productId = productId,
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
            success = f"total {newCartQuantity} {unit} {productName} in the cart"
        )

@app.route("/cart" , methods =["GET"])
def cartGetRoute():
    return redirect("/")

@app.route("/cart" , methods =["POST"])
def cartPostRoute():
    print("Rendeirng Cart from cart route...")
    print(request.form)
   
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username , password)
    if(not isinstance(user, str)):
        if(request.form["action"] == "DELETEALL"):
            return deleteAllItemInCart(request=request, user = user)
        if(request.form["action"] == "DELETE"):
            return deleteItemFromCart(request, user)
        cart = getUserCartFromUserIdDB(user.id)
        products = {}
        grandTotal = 0
        for item in cart:
            product = getProdcutByProductId(id=item.product_id)
            products[product.id] = product
            grandTotal += product.price * item.quantity
        
        cart = sorted(cart, key=lambda x: products[x.product_id].name)
        return render_template(
            "user_screens/cart.html",
            username = user.username,
            password = user.password,
            cart = cart,
            user = user,
            products = products,
            grandTotal = grandTotal
        ) 
    else:
        return redirect("/")


def deleteAllItemInCart(request, user):
    if(deleteAllItemFromCartForAUser(user.id)):
        if(not isinstance(user, str)):
            cart = getUserCartFromUserIdDB(user.id)
            products = {}
            grandTotal = 0
            for item in cart:
                product = getProdcutByProductId(id=item.product_id)
                products[product.id] = product
                grandTotal += product.price * item.quantity
            cart = sorted(cart, key=lambda x: products[x.product_id].name)
            return render_template(
                "user_screens/cart.html",
                username = user.username,
                password = user.password,
                cart = cart,
                user = user,
                products = products,
                grandTotal = grandTotal
            ) 
        else:
            return redirect("/")


def deleteItemFromCart(request, user):
    cartEntry = deleteItemFromCartDB(id=request.form["cartId"])
    cart = getUserCartFromUserIdDB(user.id)
    if(isinstance(cartEntry , str)):
        
        return render_template(
        "user_screens/cart.html",
        username = user.username,
        password = user.password,
        error = cart,
        user = user,
        cart = []
        ) 
    else:
        products = {}
        grandTotal = 0
        for item in cart:
            product = getProdcutByProductId(id=item.product_id)
            products[product.id] = product
            grandTotal += product.price * item.quantity
        cart = sorted(cart, key=lambda x: products[x.product_id].name)
        return render_template(
        "user_screens/cart.html",
        username = user.username,
        password = user.password,
        cart = cart,
        user = user,
        products = products,
        grandTotal = grandTotal
        ) 
    
@app.route("/profile" , methods =["GET"])
def profileGetRoute():
    return redirect("/")


@app.route("/profile" , methods =["POST"])
def profilePostRoute():
    print("Profile post route")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username=username , password=password)
    if(isinstance(user, str)):
        redirect('/')
    else:
        history = getLogsWithUserId(user.id)
        history = reversed(history)
        return render_template(
            "user_screens/user_profile.html",
            user = user,
            logs = history,
        )

class OrderedProduct:
    def __init__(self, name , unit , price , quantity):
        self.name = name
        self.unit = unit
        self.price = price
        self.quantity = quantity 

@app.route("/orderconfirm" , methods =["GET"])
def orderConfirmGetRoute():
    redirect("/")


@app.route("/orderconfirm" , methods =["POST"])
def orderConfirmPostRoute():
    print("Order Confirm Route Request")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username=username , password=password)

    if(isinstance(user, str)):
        redirect('/')
    else:
        if(request.form["action"] == "BUYNOW"):
            return buyOneProductRoute(request=request, user = user)
        cart = getUserCartFromUserIdDB(user.id)
        products = {}
        grandTotal = 0
        for item in cart:
            product = getProdcutByProductId(id=item.product_id)
            products[product.id] = product
            grandTotal += product.price * item.quantity
        
        buyAll = buyAllFromCartDB(user.id)
        cart = sorted(cart, key=lambda x: products[x.product_id].name)

        if(isinstance(buyAll, str)):  
            return render_template(
                "user_screens/cart.html",
                username = user.username,
                password = user.password,
                cart = cart,
                user = user,
                products = products,
                grandTotal = grandTotal,
                error = buyAll,
            ) 
        else:
            orderedProducts = []
            for item in cart:
                orderedProducts.append(
                    OrderedProduct(
                    name = item.product_name,
                    unit = products[item.product_id].unit,
                    price =  products[item.product_id].price,
                    quantity = item.quantity
                    )
                )
            return render_template(
                "user_screens/thanks_to_buy.html",
                user = user,
                grandTotal = grandTotal,
                orderedProducts = orderedProducts,
                date = datetime.now().date()
            )
        
def buyOneProductRoute(request, user):
    quantity = request.form["cartQuantity"]
    productId = request.form["productId"]
    price = request.form["price"]
    
    products = {}
        
    grandTotal = int(quantity) * int(price)
    buy = buyOneProductDB(
        userId=user.id,
        productId=productId,
        productQuantity=quantity,
    )
    if(isinstance(buy, str)):
        categories = getAllCategories()
        products = {}
        for category in categories:
            tempProds = getProductsWithCategoryId(category.id)
            products[category.id] = tempProds
        return render_template(
            "user_screens/user_dashboard.html", 
            username = user.username,
            password = user.password, 
            userId = user.id,
            categories=categories,
            products = products, 
            error=buy,
        )
    else:
        product = getProdcutByProductId(id=productId)
        orderedProducts = [
        OrderedProduct(
            name = product.name,
            unit = product.unit,
            price =product.price,
            quantity = quantity
        )]

        print(orderedProducts[0].name)
                
        return render_template(
            "user_screens/thanks_to_buy.html",
            user = user,
            grandTotal = grandTotal,
            orderedProducts = orderedProducts,
            date = datetime.now().date()
        )
        
        

        


@app.route("/buynow" , methods =["GET"])
def BuyNowGetRoute():
    return redirect("/")

@app.route("/buynow" , methods =["POST"])
def BuyNowPostRoute():
    print("Buy Now Product Request...")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username , password)
    productId = request.form["productId"]
    productName = request.form["productName"]
    unit = request.form["unit"] 
    price = request.form["price"]
    quantity = request.form["quantity"]
    manufactureDate = request.form["manufactureDate"]
    expiryDate = request.form["expiryDate"]
    if isinstance(user , str):
        return redirect("/" )

    return render_template(
        "user_screens/buy_now.html", 
        username=user.username, 
        password = user.password, 
        userId = user.id,
        productName =productName,
        unit =unit, 
        price =price, 
        quantity =quantity, 
        productId = productId,
        manufactureDate = manufactureDate,
        expiryDate = expiryDate,
    )




@app.route("/editprofile" , methods =["GET"])
def EditUserProfileGetRoute():
    return redirect("/")

@app.route("/editprofile" , methods =["POST"])
def EditUserProfilePostRoute():
    print("Edit user Profile route....")
    print(request.form)
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(
        username=username,
        password=password,
    )
    if(request.form["action"] == "EDITPROFILE"):
        return EditProfile(request , user)
    return render_template(
        "user_screens/edit_user_profile.html",
        user = user,
    ) 

def EditProfile(request , user):
    print("Action EDITPROFILE envoked...")
    newUsername = request.form["newUsername"]
    newPassword = request.form["newPassword"]
    newAddress = request.form["newAddress"]
    newPhone = request.form["newPhone"]
    newUser = editProfileDB(
        newUsername = newUsername,
        newPassword = newPassword,
        newAddress = newAddress,
        newPhone = newPhone,
        user = user,
    )

    # print(newUser.username)

    if isinstance(newUser , str):
        return render_template(
            "user_screens/edit_user_profile.html",
            user = user,
            error = newUser,
        ) 
    else:
        return render_template(
            "user_screens/edit_user_profile.html",
            user = newUser,
            success = "New changes saved",
        )
    

@app.route("/search" , methods =["GET"])
def SearchProductGetRoute():
    return redirect("/")

@app.route("/search" , methods =["POST"])
def SearchProductPostRoute():
    username = request.form["username"]
    password = request.form["password"]
    user = authUserDB(username=username, password=password)
    if(isinstance(user, str)):
        return redirect("/")
    if(request.form["action"] == "SEARCH"):
        key = request.form["key"]
        products , categories = searchItemDB(
            key = key
        )
        print(categories)
        print(products)
        return render_template(
            "user_screens/search.html",
            user = user,
            products= products,
            categories = categories,
        )
    return render_template(
        "user_screens/search.html",
        user = user,
    )
