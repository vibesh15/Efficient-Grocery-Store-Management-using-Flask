
from flask import render_template,redirect
from database.configdb import *
from database.db_controller import *
from datetime import datetime ,  timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import request
from flask import current_app as app
import io
import base64
import threading
# import thread6 as thread


@app.route("/manager" , methods=["GET"])
def managerLoginRoute():
    return render_template("manager_screens/manager_login.html", error=None)


@app.route("/manager" , methods=["POST"])
def managerLoginRoutePost():

    print(request.form)
    try:
        if(request.form["action"] == "DELETECATEGORY"):
            print("DELETECATEGORY aciton invoked....")
            return DeleteCategoryRoute(request)
        elif(request.form["action"] == "DELETEPROD"):
            print("DELETEPROD action invoeked...")
            return deleteProductRoute(
                request=request,
                manager = loginAdmin(
                    request.form["username"], 
                    request.form["password"],
                )
            )
    except Exception as e:
        print(e)
    managername = request.form["username"]
    password = request.form["password"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        categories = getAllCategories()
        products = {}
        for category in categories:
            tempProds = getProductsWithCategoryId(category.id)
            products[category.id] = tempProds
        print(products)
        return render_template(
            "manager_screens/manager_dashboard.html" , 
            managername=manager.managername, 
            password=manager.password , 
            categories=categories,
            products = products
        )
    else:
        return render_template("manager_screens/manager_login.html" , error="Invalid Credentials")

def DeleteCategoryRoute(request):
    print("Delete Category Request...")
    managername = request.form["username"]
    password = request.form["password"]
    categoryId = request.form["categoryId"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        category = deleteCateogry(categoryId)
        categories = getAllCategories()
        # categories = None
        if not category == None:
            return render_template(
                "manager_screens/manager_dashboard.html" , 
                managername=manager.managername, 
                password=manager.password , 
                categories=categories,
            )
        else:
            return render_template(
                "manager_screens/manager_dashboard.html" , 
                managername=manager.managername, 
                password=manager.password , 
                categories=categories,
            )
    else:
        return render_template("manager_screens/manager_login.html" , error="Invalid Credentials")


@app.route("/manager/summary" , methods=["GET"])
def managerSummaryRoute():
    return redirect("/manager")
    

@app.route("/manager/summary" , methods=["POST"])
def managerSummaryPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    manager = loginAdmin(managername, password)
    plotPathProduct = None
    plotPathCategory = None
    logs = getAllLogs()
    if not manager == None:
        return generate_and_render_plot(manager=manager , logs=logs)
    else:
        return redirect("/manager")


def generate_and_render_plot(manager , logs):
    
    endDate = datetime.now()
    startDate = endDate - timedelta(days=6)
    productSales = {}
    categorySales = {}
    for log in logs:
        productSales[log.product_name.upper()] = 0
        categorySales[log.category_name.upper()] = 0
    
    for log in logs:
        entryDate = datetime.strptime(log.date, '%Y-%m-%d')
        if startDate <= entryDate <= endDate:
            productSales[log.product_name.upper()] += log.quantity
            categorySales[log.category_name.upper()] += log.quantity
    
    product_names = list(productSales.keys())
    sales_data = list(productSales.values())
    plotPathProduct = None

    categoryNames = list(categorySales.keys())
    categorySalesData = list(categorySales.values())
    plotPathCategory = None
    
    with plt.style.context('dark_background'):
        plt.bar(product_names, sales_data, color="grey")
        plt.xlabel("Products")
        plt.ylabel("Sales")
        plt.title("Sales of Products")
        plt.xticks(rotation=20)
        plt.savefig("static/product_sales.png")
        plt.close()


    with plt.style.context('dark_background'):
        plt.bar(categoryNames, categorySalesData, color="grey")
        plt.xlabel("Products")
        plt.ylabel("Sales")
        plt.title("Sales of Product Category Wise")
        plt.xticks(rotation=20)
        plt.savefig("static/category_sales.png")
        plt.close()
    return render_template(
        "manager_screens/summary.html", 
        managername=manager.managername, 
        password=manager.password,
        logs = reversed(logs),
        categoryPath = plotPathCategory,
        productPath = plotPathProduct,
        isLoading = False,
    )
    


@app.route("/manager/newcategory" , methods=["GET"])
def NewCatrgoryRoute():
    return redirect("/manager")


@app.route("/manager/newcategory" , methods=["POST"])
def NewCatrgoryPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        return render_template(
            "manager_screens/create_new_category.html" , 
            managername=manager.managername, 
            password=manager.password,
        )
    else:
        return redirect("/manager")


@app.route("/manager/createnewcategory" , methods=["GET"])
def CreateNewCategoryGetRoute():
    redirect("/manager")


@app.route("/manager/createnewcategory" , methods=["POST"])
def CreateNewCategoryPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    category = request.form["category"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        category = createNewCategory(category)
        if( category == "Already Exists" ):
            return render_template(
                "manager_screens/create_new_category.html" , 
                managername=manager.managername, 
                password=manager.password, 
                error="Already Exists",
                
            )
        elif not category == None:
            return render_template(
                "manager_screens/create_new_category.html" , 
                managername=manager.managername, 
                password=manager.password, 
                success="One Category Added",
            )
         
        else:
            return render_template(
                "manager_screens/create_new_category.html" , 
                managername=manager.managername, 
                password=manager.password, 
                error="Some Error Occured",
            )
    else:
        return redirect("/manager")

@app.route("/manager/editcategory" , methods=["GET"])
def EditCategoryGetRoute():
    return redirect("/manager")

@app.route("/manager/editcategory" , methods=["POST"])
def EditCategoryPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    category = request.form["category"]
    categoryId = request.form["categoryId"]
    manager = loginAdmin(managername, password)
    if manager == None:
        return redirect("/manager")
    else:
        try:
            if(request.form["action"] == "EDITCATEGORY"):
                return editCategoryRoute(req=request , manager = manager)
        except Exception as e:
            pass
        
        return render_template(
            "manager_screens/edit_category.html",
            managername=manager.managername, 
            password=manager.password, 
            categoryId = categoryId,
            categoryName = category,
        )
        
def editCategoryRoute(req , manager):
    categoryName = req.form["category"]
    categoryId = req.form["categoryId"]
    category = editCategory(
        id=categoryId, 
        name = categoryName,
    )
    if(category == "Category not found!" or category == "Some error occured"):
        return render_template(
            "manager_screens/edit_category.html",
            managername=manager.managername, 
            password=manager.password, 
            categoryId = categoryId,
            categoryName = categoryName,
            error= category,
        )
    else:
        return render_template(
            "manager_screens/edit_category.html",
            managername=manager.managername, 
            password=manager.password, 
            categoryId = categoryId,
            categoryName = categoryName,
            success= "Category Edited Successfully",
        )


@app.route("/manager/newproduct" , methods=["GET"])
def NewProductGetRoute():
    return redirect("/manager")


@app.route("/manager/newproduct" , methods=["POST"])
def NewProductPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        try:
            if(request.form["action"] == "ADDPROD"):
                print("Add product action invoked....")
                return AddNewProduct(request)
        except Exception as e:
            print(e)
        categoryName = request.form["categoryName"]
        categoryId = request.form["categoryId"]
        return render_template(
            "manager_screens/create_new_product.html" , 
            managername=manager.managername, 
            password=manager.password, 
            categoryName=categoryName, 
            categoryId=categoryId
        )
    else:
        return redirect("/manager")

def AddNewProduct(request):
    print("Add New Product Request...")
    print(request.form)
    productName = request.form["productName"]
    categoryId = request.form["categoryId"]
    unit = request.form["unit"]
    manufactureDate = request.form["manufactureDate"]
    expiryDate = request.form["expiryDate"]
    price = int(request.form["price"])
    quantity = int(request.form["quantity"])
    managername = request.form["username"]
    password = request.form["password"]
    categoryName = request.form["categoryName"]
    try:
        print(" In route : Add New Product Request...")
        prod = addNewProductDB(
            prdName = productName , 
            category = categoryId , 
            price = price, 
            quantity = quantity , 
            unit = unit,
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
        )
   
        if not isinstance(prod , str):
            return render_template(
                "manager_screens/create_new_product.html",
                success="One Product Added",
                managername=managername, 
                password=password, 
                categoryName=categoryName, 
                categoryId=categoryId

            )
        else:
            return render_template( 
                "manager_screens/create_new_product.html", 
                error=prod,
                managername=managername, 
                password=password, 
                categoryName=categoryName, 
                categoryId=categoryId
            )
    except Exception as e:
        return render_template( 
            "manager_screens/create_new_product.html", 
            error="Some Error Occured",
            managername=managername, 
            password=password, 
            categoryName=categoryName, 
            categoryId=categoryId
        )


@app.route("/manager/editproduct" , methods=["GET"])
def EditProductGetRoute():
    redirect("/manager")

@app.route("/manager/editproduct" , methods=["POST"])
def EditProductPostRoute():
    print(request.form)
    managername = request.form["username"]
    password = request.form["password"]
    manager = loginAdmin(managername, password)
    if not manager == None:
        try:
            if( request.form["action"] == "EDITPRODUCT" ):
                return editProcuct(request=request , manager=manager)
            else:
                pass
        except Exception as e:
            pass
        categoryName = request.form["categoryName"]
        categoryId = request.form["categoryId"]
        productName = request.form["productName"]
        unit = request.form["unit"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        productId = request.form["productId"]
        manufactureDate = request.form["manufactureDate"]
        expiryDate = request.form["expiryDate"]
         
        return render_template(
            "manager_screens/edit_product.html" , 
            managername=manager.managername, 
            password=manager.password, 
            categoryName=categoryName, 
            categoryId=categoryId,
            productName =productName,
            unit =unit, 
            price =price, 
            quantity =quantity, 
            productId = productId,
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
        )
    else:
        return redirect("/manager")


def editProcuct(request , manager):
    print("Edit product route request..")
    categoryName = request.form["categoryName"]
    categoryId = request.form["categoryId"]
    productName = request.form["productName"]
    unit = request.form["unit"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    productId = request.form["productId"]
    manufactureDate = request.form["manufactureDate"]
    expiryDate = request.form["expiryDate"]
    print("Manufacture Date: ",manufactureDate)
    try:
        prod = editPrductWithProductId(
            id=productId , 
            unit=unit , 
            quantity=quantity , 
            productName= productName , 
            price= price,
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
        )
        print(prod)
        if(isinstance(prod , str)):
            return render_template(
                "manager_screens/edit_product.html" , 
                managername=manager.managername, 
                password=manager.password, 
                categoryName=categoryName, 
                categoryId=categoryId,
                productName =productName,
                unit =unit, 
                price =price, 
                quantity =quantity, 
                productId = productId,
                error = prod,
                manufacturerDate = manufactureDate,
                expiryDate = expiryDate,
            )
        else:
            return render_template(
                "manager_screens/edit_product.html" , 
                managername=manager.managername, 
                password=manager.password, 
                categoryName=categoryName, 
                categoryId=categoryId,
                productName =productName,
                unit =unit, 
                price =price, 
                quantity =quantity, 
                productId = productId,
                success = "Product Edited Successfully",
                manufacturerDate = manufactureDate,
                expiryDate = expiryDate,
            )
    except Exception as e:
        return render_template(
            "manager_screens/edit_product.html" , 
            managername=manager.managername, 
            password=manager.password, 
            categoryName=categoryName, 
            categoryId=categoryId,
            productName =productName,
            unit =unit, 
            price =price, 
            quantity =quantity, 
            productId = productId,
            error="Some Error Occured",
            manufactureDate = manufactureDate,
            expiryDate = expiryDate,
        )


def deleteProductRoute(request , manager):
    print("In Route Deleting Product")
    productId = request.form["productId"]
    categoryName = request.form["categoryName"]
    categoryId = request.form["categoryId"]
    productName = request.form["productName"]
    unit = request.form["unit"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    manufactureDate = request.form["manufactureDate"]
    expityDate = request.form["expiryDate"]
    try:
        
        if(deletePrductWithProductId(productId)):
            categories = getAllCategories()
            products = {}
            for category in categories:
                tempProds = getProductsWithCategoryId(category.id)
                products[category.id] = tempProds
            print(products)
            return render_template(
                "manager_screens/manager_dashboard.html" , 
                managername=manager.managername, 
                password=manager.password , 
                categories=categories,
                products = products
            )
        else:
            
            return render_template(
                "manager_screens/edit_product.html" , 
                managername=manager.managername, 
                password=manager.password, 
                categoryName=categoryName, 
                categoryId=categoryId,
                productName =productName,
                unit =unit, 
                price =price, 
                quantity =quantity, 
                productId = productId,
                manufactureDate = manufactureDate,
                expityDate = expityDate,
                error="Could Not delete Product"
            )

    except Exception as e:
        print(e)
        return render_template(
                "manager_screens/edit_product.html" , 
                managername=manager.managername, 
                password=manager.password, 
                categoryName=categoryName, 
                categoryId=categoryId,
                productName =productName,
                unit =unit, 
                price =price, 
                quantity =quantity, 
                productId = productId,
                manufactureDate = manufactureDate,
                expityDate = expityDate,
                error="Could Not delete Prduct"
        )
