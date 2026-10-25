import csv
import random
from faker import Faker
from datetime import datetime, timedelta

# Khởi tạo Faker
fake = Faker('vi_VN') # Sử dụng dữ liệu tiếng Việt

# Cấu hình số lượng dữ liệu cần sinh
NUM_CUSTOMERS = 10000
NUM_CATEGORIES = 10
NUM_STORES = 5
NUM_PRODUCTS = 500
NUM_ORDERS = 50000

print("Bắt đầu sinh dữ liệu...")

# 1. Sinh Categories
categories = []
with open('categories.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category_ID', 'Name', 'Description'])
    for i in range(1, NUM_CATEGORIES + 1):
        cat = [i, f"Danh mục {i}", fake.sentence(nb_words=5)]
        categories.append(cat)
        writer.writerow(cat)
print(" Đã tạo Categories")

# 2. Sinh Stores
stores = []
with open('stores.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Store_ID', 'Name', 'Address', 'City'])
    for i in range(1, NUM_STORES + 1):
        store = [i, f"Cửa hàng {i}", fake.street_address(), fake.city()]
        stores.append(store)
        writer.writerow(store)
print(" Đã tạo Stores")

# 3. Sinh Customers
customers = []
with open('customers.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Customer_ID', 'Name', 'Email', 'Phone', 'Address', 'City', 'Tier', 'Created_At'])
    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    for i in range(1, NUM_CUSTOMERS + 1):
        cust = [
            i, 
            fake.name(), 
            fake.email(), 
            fake.phone_number(), 
            fake.street_address(), 
            fake.city(), 
            random.choice(tiers), 
            fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M:%S")
        ]
        customers.append(cust)
        writer.writerow(cust)
print(" Đã tạo Customers")

# 4. Sinh Products
products = []
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product_ID', 'Name', 'Category_ID', 'Price', 'Cost_Price', 'Stock_Quantity'])
    for i in range(1, NUM_PRODUCTS + 1):
        cost_price = random.randint(10, 500) * 1000 # Giá vốn
        price = int(cost_price * random.uniform(1.2, 2.0)) # Giá bán (lãi 20% - 100%)
        prod = [
            i, 
            fake.catch_phrase(), 
            random.randint(1, NUM_CATEGORIES), 
            price, 
            cost_price, 
            random.randint(50, 1000)
        ]
        products.append(prod)
        writer.writerow(prod)
print(" Đã tạo Products")

# 5. Sinh Orders, Order_Details, Payments
with open('orders.csv', mode='w', newline='', encoding='utf-8') as f_ord, \
     open('order_details.csv', mode='w', newline='', encoding='utf-8') as f_det, \
     open('payments.csv', mode='w', newline='', encoding='utf-8') as f_pay:
    
    writer_ord = csv.writer(f_ord)
    writer_det = csv.writer(f_det)
    writer_pay = csv.writer(f_pay)
    
    writer_ord.writerow(['Order_ID', 'Customer_ID', 'Store_ID', 'Order_Date', 'Status', 'Total_Amount'])
    writer_det.writerow(['Order_Detail_ID', 'Order_ID', 'Product_ID', 'Quantity', 'Unit_Price'])
    writer_pay.writerow(['Payment_ID', 'Order_ID', 'Method', 'Amount', 'Paid_At', 'Status'])
    
    statuses = ['Completed', 'Pending', 'Canceled']
    payment_methods = ['COD', 'Credit Card', 'MoMo', 'ZaloPay']
    
    detail_id = 1
    for order_id in range(1, NUM_ORDERS + 1):
        customer_id = random.randint(1, NUM_CUSTOMERS)
        store_id = random.randint(1, NUM_STORES)
        order_date = fake.date_time_between(start_date='-1y', end_date='now')
        status = random.choices(statuses, weights=[0.8, 0.1, 0.1])[0]
        
        # Tạo chi tiết đơn hàng
        num_items = random.randint(1, 5) # Mỗi đơn có 1-5 mặt hàng
        total_amount = 0
        
        # Chọn ngẫu nhiên sản phẩm cho đơn hàng (không trùng lặp trong 1 đơn)
        selected_products = random.sample(products, num_items)
        
        for prod in selected_products:
            prod_id = prod[0]
            unit_price = prod[3] # Lấy giá bán hiện tại làm đơn giá
            quantity = random.randint(1, 3)
            
            writer_det.writerow([detail_id, order_id, prod_id, quantity, unit_price])
            total_amount += (unit_price * quantity)
            detail_id += 1
            
        writer_ord.writerow([order_id, customer_id, store_id, order_date.strftime("%Y-%m-%d %H:%M:%S"), status, total_amount])
        
        # Tạo thanh toán
        pay_status = 'Success' if status == 'Completed' else ('Pending' if status == 'Pending' else 'Failed')
        paid_at = (order_date + timedelta(minutes=random.randint(10, 1440))).strftime("%Y-%m-%d %H:%M:%S") if pay_status == 'Success' else ''
        
        writer_pay.writerow([order_id, order_id, random.choice(payment_methods), total_amount, paid_at, pay_status])
        
        if order_id % 10000 == 0:
            print(f" Đã tạo {order_id} Orders...")

print("HOÀN TẤT SINH DỮ LIỆU!")