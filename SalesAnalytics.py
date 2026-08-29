import numpy as np
import os

Data_File = "sales_data.csv"
Clean_File = "clean_sales_data.py"

data = None
clean_data = None

def generate_dataset():
    np.random.seed(42)

    n = 1000

    transcation_id = np.arrange(10001,10001+n)

    products = np.array([
        "Laptop",
        "Phone",
        "Tablet",
        "Headphones",
        "Keyboard",
        "Monitor"
    ])

    categories = np.array([
        "Electronics",
                "Electronics",
                "Electronics",
                "Accessories",
                "Accessories",
                "Electronics"
    ])

    product_index = np.random.randint(0 , len(products) , n)
    product = products[product_index]
    categorie = categories[product_index]

    quantity = np.random.randint(1,11,n)

    price_ranges = {
        "Laptop": (50000,100000),
        "Phone": (15000,80000),
        "Tablet": (10000, 50000),
        "Headphones": (1000, 15000),
        "Keyboard": (500, 5000),
        "Monitor": (8000, 40000)
    }

    price = np.zeros(n)

    for i in range(n):
        low, high = price_ranges[product[i]]
        price[i] = np.random.randint(low,high+1) 

    discount = np.round(np.random.uniform(0,0.30,n),2)

    revenue = quantity * price * ( 1 - discount)

    #Intentional Bad Data 

    quantity = quantity.astype(float)
    quantity[np.random.choice(n, 10, replace=False)] = np.nan

    # Missing prices
    price[np.random.choice(n, 8, replace=False)] = np.nan

    # Invalid negative values
    quantity[20] = -5
    price[50] = -1000

    # Invalid discount
    discount[100] = 1.5

    # Recalculate revenue after corruption
    revenue = quantity * price * (1 - discount)

    with open(Data_File, "w") as file:
    
            file.write(
                "transaction_id,product,category,quantity,price,discount,revenue\n"
            )
    
            for i in range(n):
    
                q = "" if np.isnan(quantity[i]) else str(int(quantity[i]))
                p = "" if np.isnan(price[i]) else str(round(price[i], 2))
    
                r = (
                    ""
                    if np.isnan(revenue[i])
                    else str(round(revenue[i], 2))
                )
    
                file.write(
                    f"{transcation_id[i]},"
                    f"{product[i]},"
                    f"{categorie[i]},"
                    f"{q},"
                    f"{p},"
                    f"{discount[i]},"
                    f"{r}\n"
                )
    
                print("\nDataset generated successfully!")
                print(f"File: {Data_File}")
                print(f"Records: {n}")
    
    
    # ============================================================
    # 2. LOAD DATASET
    # ============================================================
    
    def load_dataset():
    
        global data
    
        if not os.path.exists(Data_File):
            print("\nDataset not found.")
            print("Generating dataset first...")
            generate_dataset()
    
        try:
    
            data = np.genfromtxt(
                Data_File,
                delimiter=",",
                names=True,
                dtype=[
                    ("transaction_id", "i4"),
                    ("product", "U20"),
                    ("category", "U20"),
                    ("quantity", "f8"),
                    ("price", "f8"),
                    ("discount", "f8"),
                    ("revenue", "f8")
                ],
                encoding="utf-8",
                missing_values="",
                filling_values=np.nan
            )
    
            print("\nDataset loaded successfully.")
    
            print(f"Rows   : {data.shape[0]}")
            print(f"Columns: {len(data.dtype.names)}")
    
        except Exception as e:
    
            print("\nError loading dataset:")
            print(e)
    
    
    # ============================================================
    # 3. DATASET INFORMATION
    # ============================================================
    
    def dataset_information():
    
        if data is None:
            print("\nPlease load the dataset first.")
            return
    
        print("\n" + "=" * 55)
        print("DATASET INFORMATION")
        print("=" * 55)
    
        print("Rows       :", data.shape[0])
        print("Columns    :", len(data.dtype.names))
        print("Dimensions :", data.ndim)
    
        print("\nColumns:")
    
        for column in data.dtype.names:
            print(" -", column)
    
    
    # ============================================================
    # 4. VIEW RAW DATA
    # ============================================================
    
    def view_data():
    
        if data is None:
            print("\nPlease load the dataset first.")
            return
    
        print("\n" + "=" * 85)
        print("FIRST 10 TRANSACTIONS")
        print("=" * 85)
    
        print(
            f"{'ID':<8}"
            f"{'Product':<15}"
            f"{'Category':<15}"
            f"{'Qty':<8}"
            f"{'Price':<12}"
            f"{'Discount':<10}"
            f"{'Revenue':<15}"
        )
    
        print("-" * 85)
    
        for row in data[:10]:
    
            print(
                f"{int(row['transaction_id']):<8}"
                f"{row['product']:<15}"
                f"{row['category']:<15}"
                f"{row['quantity']:<8}"
                f"{row['price']:<12.2f}"
                f"{row['discount']:<10.2f}"
                f"{row['revenue']:<15.2f}"
            )
    



    