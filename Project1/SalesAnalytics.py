
import numpy as np
import os


# SALES ANALYTICS & DATA QUALITY ENGINE
# NumPy Capstone Project


DATA_FILE = "sales_data.csv"
CLEAN_FILE = "clean_sales_data.npy"


# GLOBAL DATA


data = None
clean_data = None


# 1. GENERATE SAMPLE RAW DATA


def generate_dataset():
    np.random.seed(42)

    n = 1000

    transaction_id = np.arange(10001, 10001 + n)

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

    product_index = np.random.randint(0, len(products), n)

    product = products[product_index]
    category = categories[product_index]

    quantity = np.random.randint(1, 11, n)

    price_ranges = {
        "Laptop": (50000, 100000),
        "Phone": (15000, 80000),
        "Tablet": (10000, 50000),
        "Headphones": (1000, 15000),
        "Keyboard": (500, 5000),
        "Monitor": (8000, 40000)
    }

    price = np.zeros(n)

    for i in range(n):
        low, high = price_ranges[product[i]]
        price[i] = np.random.randint(low, high + 1)

    discount = np.round(np.random.uniform(0, 0.30, n), 2)

    # Calculate revenue
    revenue = quantity * price * (1 - discount)

    
    # Introduce some bad data intentionally
   

    # Missing quantities
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

    # Save as CSV
    with open(DATA_FILE, "w") as file:

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
                f"{transaction_id[i]},"
                f"{product[i]},"
                f"{category[i]},"
                f"{q},"
                f"{p},"
                f"{discount[i]},"
                f"{r}\n"
            )

    print("\nDataset generated successfully!")
    print(f"File: {DATA_FILE}")
    print(f"Records: {n}")



# 2. LOAD DATASET


def load_dataset():

    global data

    if not os.path.exists(DATA_FILE):
        print("\nDataset not found.")
        print("Generating dataset first...")
        generate_dataset()

    try:

        data = np.genfromtxt(
            DATA_FILE,
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



# 3. DATASET INFORMATION


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


# 4. VIEW RAW DATA


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



# 5. DATA QUALITY CHECK


def data_quality_check():

    if data is None:
        print("\nPlease load the dataset first.")
        return

    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT")
    print("=" * 60)

    total_rows = len(data)

    # Missing values
    missing_quantity = np.isnan(data["quantity"]).sum()
    missing_price = np.isnan(data["price"]).sum()
    missing_revenue = np.isnan(data["revenue"]).sum()

    # Invalid values
    invalid_quantity = np.sum(data["quantity"] < 0)
    invalid_price = np.sum(data["price"] < 0)

    invalid_discount = np.sum(
        (data["discount"] < 0) |
        (data["discount"] > 1)
    )

    # Duplicate transaction IDs
    unique_ids, counts = np.unique(
        data["transaction_id"],
        return_counts=True
    )

    duplicate_ids = np.sum(counts > 1)

    print("\nTotal Records:", total_rows)

    print("\nMissing Values")
    print("----------------------")

    print("Quantity :", missing_quantity)
    print("Price    :", missing_price)
    print("Revenue  :", missing_revenue)

    print("\nInvalid Values")
    print("----------------------")

    print("Negative Quantity :", invalid_quantity)
    print("Negative Price    :", invalid_price)
    print("Invalid Discount  :", invalid_discount)

    print("\nDuplicate IDs:", duplicate_ids)

    total_issues = (
        missing_quantity
        + missing_price
        + missing_revenue
        + invalid_quantity
        + invalid_price
        + invalid_discount
    )

    print("\nTotal Data Issues:", total_issues)

    if total_issues == 0:
        print("\nData Quality: GOOD")
    else:
        print("\nData Quality: NEEDS CLEANING")



# 6. CLEAN DATA

def clean_dataset():

    global clean_data

    if data is None:
        print("\nPlease load the dataset first.")
        return

    print("\nCleaning dataset...")

    # Make a copy
    clean_data = data.copy()

    # --------------------------------------------------------
    # Replace missing quantity with median quantity
    # --------------------------------------------------------

    valid_quantity = clean_data["quantity"][
        ~np.isnan(clean_data["quantity"])
    ]

    quantity_median = np.median(valid_quantity)

    missing_quantity = np.isnan(clean_data["quantity"])

    clean_data["quantity"][missing_quantity] = quantity_median

    # --------------------------------------------------------
    # Replace missing price with median price
    # --------------------------------------------------------

    valid_price = clean_data["price"][
        ~np.isnan(clean_data["price"])
    ]

    price_median = np.median(valid_price)

    missing_price = np.isnan(clean_data["price"])

    clean_data["price"][missing_price] = price_median

    # --------------------------------------------------------
    # Fix invalid negative quantity
    # --------------------------------------------------------

    invalid_quantity = clean_data["quantity"] < 0

    clean_data["quantity"][
        invalid_quantity
    ] = quantity_median

    # --------------------------------------------------------
    # Fix invalid negative price
    # --------------------------------------------------------

    invalid_price = clean_data["price"] < 0

    clean_data["price"][
        invalid_price
    ] = price_median

    # --------------------------------------------------------
    # Fix invalid discount
    # --------------------------------------------------------

    invalid_discount = (
        (clean_data["discount"] < 0) |
        (clean_data["discount"] > 1)
    )

    clean_data["discount"][
        invalid_discount
    ] = 0

    # --------------------------------------------------------
    # Recalculate Revenue
    #
    # Broadcasting / vectorized operation
    # --------------------------------------------------------

    clean_data["revenue"] = (
        clean_data["quantity"]
        * clean_data["price"]
        * (1 - clean_data["discount"])
    )

    # Save NumPy binary file
    np.save(CLEAN_FILE, clean_data)

    print("\nCleaning completed.")

    print("Missing quantities fixed :", missing_quantity.sum())
    print("Missing prices fixed    :", missing_price.sum())
    print("Invalid quantities fixed:", invalid_quantity.sum())
    print("Invalid prices fixed    :", invalid_price.sum())
    print("Invalid discounts fixed :", invalid_discount.sum())

    print(f"\nClean dataset saved as: {CLEAN_FILE}")


# 7. SALES STATISTICS


def sales_statistics():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    print("\n" + "=" * 60)
    print("SALES STATISTICS")
    print("=" * 60)

    print(f"\nTotal Revenue : ₹{np.sum(revenue):,.2f}")

    print(
        f"Average Revenue: ₹{np.mean(revenue):,.2f}"
    )

    print(
        f"Median Revenue : ₹{np.median(revenue):,.2f}"
    )

    print(
        f"Maximum Revenue: ₹{np.max(revenue):,.2f}"
    )

    print(
        f"Minimum Revenue: ₹{np.min(revenue):,.2f}"
    )

    print(
        f"Std Deviation  : ₹{np.std(revenue):,.2f}"
    )

    print(
        f"Revenue Variance: ₹{np.var(revenue):,.2f}"
    )

    print(
        f"Total Quantity Sold: "
        f"{np.sum(clean_data['quantity']):,.0f}"
    )



# 8. TOP TRANSACTIONS

def top_transactions():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    # argsort returns indexes
    indices = np.argsort(revenue)[-10:][::-1]

    print("\n" + "=" * 75)
    print("TOP 10 TRANSACTIONS")
    print("=" * 75)

    print(
        f"{'Rank':<6}"
        f"{'Transaction':<15}"
        f"{'Product':<15}"
        f"{'Quantity':<10}"
        f"{'Revenue':<15}"
    )

    print("-" * 75)

    for rank, index in enumerate(indices, start=1):

        print(
            f"{rank:<6}"
            f"{int(clean_data['transaction_id'][index]):<15}"
            f"{clean_data['product'][index]:<15}"
            f"{clean_data['quantity'][index]:<10.0f}"
            f"₹{clean_data['revenue'][index]:<14,.2f}"
        )


# 9. PRODUCT ANALYSIS


def product_analysis():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    products, counts = np.unique(
        clean_data["product"],
        return_counts=True
    )

    print("\n" + "=" * 75)
    print("PRODUCT PERFORMANCE")
    print("=" * 75)

    print(
        f"{'Product':<20}"
        f"{'Transactions':<15}"
        f"{'Revenue':<20}"
        f"{'Avg Revenue':<15}"
    )

    print("-" * 75)

    product_revenues = []

    for product in products:

        mask = clean_data["product"] == product

        revenue = clean_data["revenue"][mask]

        total = np.sum(revenue)

        average = np.mean(revenue)

        product_revenues.append(total)

        transaction_count = np.sum(mask)

        print(
            f"{product:<20}"
            f"{transaction_count:<15}"
            f"₹{total:<19,.2f}"
            f"₹{average:<14,.2f}"
        )

    # Find best product
    best_index = np.argmax(product_revenues)

    print("\nBest Performing Product:")
    print(products[best_index])



# 10. CATEGORY ANALYSIS


def category_analysis():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    categories = np.unique(
        clean_data["category"]
    )

    print("\n" + "=" * 65)
    print("CATEGORY PERFORMANCE")
    print("=" * 65)

    for category in categories:

        mask = clean_data["category"] == category

        revenue = clean_data["revenue"][mask]

        quantity = clean_data["quantity"][mask]

        print(f"\nCategory: {category}")

        print(
            f"Transactions : {np.sum(mask)}"
        )

        print(
            f"Quantity Sold: {np.sum(quantity):,.0f}"
        )

        print(
            f"Revenue      : ₹{np.sum(revenue):,.2f}"
        )

        print(
            f"Average Sale : ₹{np.mean(revenue):,.2f}"
        )


# 11. OUTLIER DETECTION


def detect_outliers():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    mean = np.mean(revenue)
    std = np.std(revenue)

    # More than 2 standard deviations from mean
    upper_limit = mean + (2 * std)
    lower_limit = mean - (2 * std)

    outlier_mask = (
        (revenue > upper_limit) |
        (revenue < lower_limit)
    )

    outliers = clean_data[outlier_mask]

    print("\n" + "=" * 65)
    print("OUTLIER DETECTION")
    print("=" * 65)

    print(f"\nMean Revenue : ₹{mean:,.2f}")
    print(f"Std Deviation: ₹{std:,.2f}")

    print(f"\nUpper Limit  : ₹{upper_limit:,.2f}")
    print(f"Lower Limit  : ₹{lower_limit:,.2f}")

    print(
        f"\nPotential Outliers: {len(outliers)}"
    )

    if len(outliers) > 0:

        print("\nTop Outliers:")

        indices = np.argsort(
            outliers["revenue"]
        )[-5:][::-1]

        for index in indices:

            print(
                f"Transaction "
                f"{int(outliers['transaction_id'][index])}"
                f" → ₹"
                f"{outliers['revenue'][index]:,.2f}"
            )



# 12. CUSTOMER / SALES SEGMENTATION


def sales_segmentation():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    # np.where creates categories
    segment = np.where(
        revenue >= 50000,
        "High",
        np.where(
            revenue >= 20000,
            "Medium",
            "Low"
        )
    )

    high = np.sum(segment == "High")
    medium = np.sum(segment == "Medium")
    low = np.sum(segment == "Low")

    print("\n" + "=" * 55)
    print("SALES SEGMENTATION")
    print("=" * 55)

    print("\nHigh Value Transactions  :", high)
    print("Medium Value Transactions:", medium)
    print("Low Value Transactions   :", low)

    print("\nPercentage Distribution:")

    total = len(segment)

    print(
        f"High   : {high / total * 100:.2f}%"
    )

    print(
        f"Medium : {medium / total * 100:.2f}%"
    )

    print(
        f"Low    : {low / total * 100:.2f}%"
    )


# 13. BUSINESS INSIGHTS


def business_insights():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    products = np.unique(
        clean_data["product"]
    )

    product_totals = []

    for product in products:

        mask = clean_data["product"] == product

        total = np.sum(
            clean_data["revenue"][mask]
        )

        product_totals.append(total)

    product_totals = np.array(product_totals)

    best_product = products[
        np.argmax(product_totals)
    ]

    worst_product = products[
        np.argmin(product_totals)
    ]

    print("\n" + "=" * 65)
    print("BUSINESS INSIGHTS")
    print("=" * 65)

    print(
        f"\n1. Total Revenue: "
        f"₹{np.sum(revenue):,.2f}"
    )

    print(
        f"2. Best Product: "
        f"{best_product}"
    )

    print(
        f"3. Lowest Revenue Product: "
        f"{worst_product}"
    )

    print(
        f"4. Average Transaction Value: "
        f"₹{np.mean(revenue):,.2f}"
    )

    high_value = np.sum(revenue >= 50000)

    print(
        f"5. High Value Transactions: "
        f"{high_value}"
    )

    print(
        f"6. Total Units Sold: "
        f"{np.sum(clean_data['quantity']):,.0f}"
    )

    print(
        "\nRecommendation:"
    )

    print(
        f"Focus marketing and inventory "
        f"optimization around {best_product}."
    )


# 14. SAVE CLEAN DATA AS TEXT


def export_clean_data():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    output_file = "clean_sales_data.csv"

    numeric_data = np.column_stack([
        clean_data["transaction_id"],
        clean_data["quantity"],
        clean_data["price"],
        clean_data["discount"],
        clean_data["revenue"]
    ])

    np.savetxt(
        output_file,
        numeric_data,
        delimiter=",",
        header="transaction_id,quantity,price,discount,revenue",
        comments="",
        fmt="%.2f"
    )

    print(
        f"\nClean numerical data exported to: "
        f"{output_file}"
    )



# 15. LOAD SAVED NUMPY DATA


def load_saved_numpy_data():

    if not os.path.exists(CLEAN_FILE):

        print(
            "\nNo saved NumPy dataset found."
        )

        return

    loaded = np.load(
        CLEAN_FILE,
        allow_pickle=True
    )

    print("\nSaved NumPy dataset loaded.")

    print(
        "Rows:",
        loaded.shape[0]
    )

    print(
        "Columns:",
        loaded.dtype.names
    )



# 16. COMPLETE REPORT


def complete_report():

    if clean_data is None:
        print("\nPlease clean the dataset first.")
        return

    revenue = clean_data["revenue"]

    print("\n")
    print("=" * 70)
    print("              FINAL SALES ANALYTICS REPORT")
    print("=" * 70)

    print("\nDATASET")
    print("-" * 70)

    print(
        "Total Transactions :",
        len(clean_data)
    )

    print(
        "Unique Products     :",
        len(np.unique(clean_data["product"]))
    )

    print(
        "Unique Categories   :",
        len(np.unique(clean_data["category"]))
    )

    print("\nREVENUE")
    print("-" * 70)

    print(
        f"Total Revenue       : ₹{np.sum(revenue):,.2f}"
    )

    print(
        f"Average Revenue     : ₹{np.mean(revenue):,.2f}"
    )

    print(
        f"Median Revenue      : ₹{np.median(revenue):,.2f}"
    )

    print(
        f"Highest Transaction : ₹{np.max(revenue):,.2f}"
    )

    print(
        f"Lowest Transaction  : ₹{np.min(revenue):,.2f}"
    )

    print("\nOPERATIONS")
    print("-" * 70)

    print(
        f"Total Units Sold    : "
        f"{np.sum(clean_data['quantity']):,.0f}"
    )

    print(
        f"Average Quantity    : "
        f"{np.mean(clean_data['quantity']):.2f}"
    )

    print("\nTOP PRODUCTS")
    print("-" * 70)

    products = np.unique(
        clean_data["product"]
    )

    product_revenues = []

    for product in products:

        mask = clean_data["product"] == product

        total = np.sum(
            clean_data["revenue"][mask]
        )

        product_revenues.append(total)

    sorted_indices = np.argsort(
        product_revenues
    )[::-1]

    for rank, index in enumerate(
        sorted_indices[:3],
        start=1
    ):

        print(
            f"{rank}. "
            f"{products[index]} → "
            f"₹{product_revenues[index]:,.2f}"
        )

    print("\n" + "=" * 70)
    print("             END OF REPORT")
    print("=" * 70)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 60)
        print("       SALES ANALYTICS & DATA QUALITY ENGINE")
        print("=" * 60)

        print("\n1. Generate Dataset")
        print("2. Load Dataset")
        print("3. Dataset Information")
        print("4. View Raw Data")
        print("5. Data Quality Check")
        print("6. Clean Dataset")
        print("7. Sales Statistics")
        print("8. Top 10 Transactions")
        print("9. Product Analysis")
        print("10. Category Analysis")
        print("11. Detect Outliers")
        print("12. Sales Segmentation")
        print("13. Business Insights")
        print("14. Export Clean Data")
        print("15. Load Saved NumPy Data")
        print("16. Complete Final Report")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            generate_dataset()

        elif choice == "2":
            load_dataset()

        elif choice == "3":
            dataset_information()

        elif choice == "4":
            view_data()

        elif choice == "5":
            data_quality_check()

        elif choice == "6":
            clean_dataset()

        elif choice == "7":
            sales_statistics()

        elif choice == "8":
            top_transactions()

        elif choice == "9":
            product_analysis()

        elif choice == "10":
            category_analysis()

        elif choice == "11":
            detect_outliers()

        elif choice == "12":
            sales_segmentation()

        elif choice == "13":
            business_insights()

        elif choice == "14":
            export_clean_data()

        elif choice == "15":
            load_saved_numpy_data()

        elif choice == "16":
            complete_report()

        elif choice == "0":
            print("\nExiting Sales Analytics Engine...")
            print("Thank you!")
            break

        else:
            print("\nInvalid choice. Please try again.")



# PROGRAM START


if __name__ == "__main__":
    main()

