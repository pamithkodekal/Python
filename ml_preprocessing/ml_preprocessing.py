
import numpy as np
import os
import time


# ============================================================
# ML DATA PREPROCESSING ENGINE
# NumPy Project 2
# ============================================================

RAW_FILE = "employee_data.csv"
PROCESSED_FILE = "processed_data.npy"
TRAIN_FILE = "train_data.npy"
TEST_FILE = "test_data.npy"
EXPORT_FILE = "processed_data.csv"

data = None
features = None
target = None

X_train = None
X_test = None
y_train = None
y_test = None

normalized_data = None
standardized_data = None


# ============================================================
# 1. GENERATE DATASET
# ============================================================

def generate_dataset():

    np.random.seed(42)

    n = 500

    employee_id = np.arange(1001, 1001 + n)

    age = np.random.randint(21, 51, n)

    experience = np.random.randint(0, 21, n)

    projects = np.random.randint(1, 21, n)

    working_hours = np.random.randint(30, 61, n)

    salary = (
        25000
        + experience * 5000
        + projects * 1500
        + np.random.randint(-5000, 5001, n)
    )

    salary = np.maximum(salary, 20000)

    performance_score = np.round(
        np.random.uniform(40, 100, n),
        2
    )

    # --------------------------------------------------------
    # Introduce some missing values
    # --------------------------------------------------------

    age = age.astype(float)
    experience = experience.astype(float)
    salary = salary.astype(float)
    performance_score = performance_score.astype(float)

    age[np.random.choice(n, 5, replace=False)] = np.nan

    experience[np.random.choice(n, 5, replace=False)] = np.nan

    salary[np.random.choice(n, 5, replace=False)] = np.nan

    # --------------------------------------------------------
    # Create CSV
    # --------------------------------------------------------

    with open(RAW_FILE, "w") as file:

        file.write(
            "employee_id,age,experience,projects,"
            "working_hours,salary,performance_score\n"
        )

        for i in range(n):

            age_value = (
                ""
                if np.isnan(age[i])
                else str(int(age[i]))
            )

            experience_value = (
                ""
                if np.isnan(experience[i])
                else str(int(experience[i]))
            )

            salary_value = (
                ""
                if np.isnan(salary[i])
                else str(round(salary[i], 2))
            )

            performance_value = str(
                performance_score[i]
            )

            file.write(
                f"{employee_id[i]},"
                f"{age_value},"
                f"{experience_value},"
                f"{projects[i]},"
                f"{working_hours[i]},"
                f"{salary_value},"
                f"{performance_value}\n"
            )

    print("\n" + "=" * 60)
    print("DATASET GENERATED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nFile    : {RAW_FILE}")
    print(f"Records : {n}")


# ============================================================
# 2. LOAD DATASET
# ============================================================

def load_dataset():

    global data

    if not os.path.exists(RAW_FILE):

        print("\nDataset not found.")
        print("Generating dataset...")

        generate_dataset()

    try:

        data = np.genfromtxt(
            RAW_FILE,
            delimiter=",",
            names=True,
            dtype=[
                ("employee_id", "i4"),
                ("age", "f8"),
                ("experience", "f8"),
                ("projects", "f8"),
                ("working_hours", "f8"),
                ("salary", "f8"),
                ("performance_score", "f8")
            ],
            encoding="utf-8",
            missing_values="",
            filling_values=np.nan
        )

        print("\nDataset loaded successfully.")

        print("Rows   :", data.shape[0])
        print("Columns:", len(data.dtype.names))

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

    print("\n" + "=" * 60)
    print("DATASET INFORMATION")
    print("=" * 60)

    print("\nRows       :", data.shape[0])
    print("Dimensions :", data.ndim)
    print("Columns    :", len(data.dtype.names))

    print("\nColumn Names:")

    for column in data.dtype.names:

        print("-", column)

    print("\nData Types:")

    for column in data.dtype.names:

        print(
            f"{column:<20} "
            f"{data[column].dtype}"
        )


# ============================================================
# 4. VIEW DATA
# ============================================================

def view_data():

    if data is None:

        print("\nPlease load the dataset first.")

        return

    print("\n" + "=" * 90)
    print("FIRST 10 EMPLOYEES")
    print("=" * 90)

    print(
        f"{'ID':<8}"
        f"{'Age':<8}"
        f"{'Exp':<8}"
        f"{'Projects':<10}"
        f"{'Hours':<10}"
        f"{'Salary':<15}"
        f"{'Performance':<12}"
    )

    print("-" * 90)

    for row in data[:10]:

        print(
            f"{int(row['employee_id']):<8}"
            f"{row['age']:<8.0f}"
            f"{row['experience']:<8.0f}"
            f"{row['projects']:<10.0f}"
            f"{row['working_hours']:<10.0f}"
            f"₹{row['salary']:<14,.2f}"
            f"{row['performance_score']:<12.2f}"
        )


# ============================================================
# 5. DATA QUALITY CHECK
# ============================================================

def data_quality_check():

    if data is None:

        print("\nPlease load the dataset first.")

        return

    print("\n" + "=" * 60)
    print("DATA QUALITY CHECK")
    print("=" * 60)

    total_missing = 0

    numeric_columns = [
        "age",
        "experience",
        "projects",
        "working_hours",
        "salary",
        "performance_score"
    ]

    print("\nMissing Values")
    print("-" * 40)

    for column in numeric_columns:

        missing = np.isnan(
            data[column]
        ).sum()

        total_missing += missing

        print(
            f"{column:<20}: {missing}"
        )

    print("\nTotal Missing Values:", total_missing)

    # Check duplicate IDs

    ids, counts = np.unique(
        data["employee_id"],
        return_counts=True
    )

    duplicate_ids = np.sum(
        counts > 1
    )

    print(
        "\nDuplicate Employee IDs:",
        duplicate_ids
    )

    # Check invalid values

    negative_salary = np.sum(
        data["salary"] < 0
    )

    invalid_performance = np.sum(
        (data["performance_score"] < 0)
        |
        (data["performance_score"] > 100)
    )

    print(
        "Negative Salaries:",
        negative_salary
    )

    print(
        "Invalid Performance Scores:",
        invalid_performance
    )


# ============================================================
# 6. CLEAN DATA
# ============================================================

def clean_data():

    global features
    global target

    if data is None:

        print("\nPlease load the dataset first.")

        return

    print("\nCleaning data...")

    # --------------------------------------------------------
    # Create numerical feature matrix
    # --------------------------------------------------------

    features = np.column_stack([
        data["age"],
        data["experience"],
        data["projects"],
        data["working_hours"],
        data["performance_score"]
    ])

    # Salary is target

    target = data["salary"].copy()

    # --------------------------------------------------------
    # Replace missing values with column median
    # --------------------------------------------------------

    for column in range(features.shape[1]):

        column_data = features[:, column]

        valid_values = column_data[
            ~np.isnan(column_data)
        ]

        median_value = np.median(
            valid_values
        )

        missing_mask = np.isnan(
            column_data
        )

        features[
            missing_mask,
            column
        ] = median_value

    # --------------------------------------------------------
    # Replace missing target values
    # --------------------------------------------------------

    valid_target = target[
        ~np.isnan(target)
    ]

    target_median = np.median(
        valid_target
    )

    missing_target = np.isnan(
        target
    )

    target[missing_target] = target_median

    print("\nCleaning completed.")

    print(
        "Feature Matrix Shape:",
        features.shape
    )

    print(
        "Target Shape:",
        target.shape
    )


# ============================================================
# 7. NORMALIZATION
# ============================================================

def normalize_features():

    global normalized_data

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    minimum = np.min(
        features,
        axis=0
    )

    maximum = np.max(
        features,
        axis=0
    )

    # Avoid division by zero

    denominator = maximum - minimum

    denominator[
        denominator == 0
    ] = 1

    normalized_data = (
        features - minimum
    ) / denominator

    print("\n" + "=" * 60)
    print("NORMALIZATION COMPLETED")
    print("=" * 60)

    print(
        "\nMinimum values:",
        minimum
    )

    print(
        "\nMaximum values:",
        maximum
    )

    print(
        "\nFirst 5 normalized rows:"
    )

    print(
        normalized_data[:5]
    )


# ============================================================
# 8. STANDARDIZATION
# ============================================================

def standardize_features():

    global standardized_data

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    mean = np.mean(
        features,
        axis=0
    )

    std = np.std(
        features,
        axis=0
    )

    # Avoid division by zero

    std[
        std == 0
    ] = 1

    standardized_data = (
        features - mean
    ) / std

    print("\n" + "=" * 60)
    print("STANDARDIZATION COMPLETED")
    print("=" * 60)

    print(
        "\nMean:",
        mean
    )

    print(
        "\nStandard Deviation:",
        std
    )

    print(
        "\nFirst 5 standardized rows:"
    )

    print(
        standardized_data[:5]
    )


# ============================================================
# 9. TRAIN / TEST SPLIT
# ============================================================

def train_test_split_data():

    global X_train
    global X_test
    global y_train
    global y_test

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    # --------------------------------------------------------
    # Shuffle indices
    # --------------------------------------------------------

    np.random.seed(42)

    indices = np.random.permutation(
        len(features)
    )

    shuffled_features = features[
        indices
    ]

    shuffled_target = target[
        indices
    ]

    # --------------------------------------------------------
    # 80 / 20 split
    # --------------------------------------------------------

    split_index = int(
        0.8 * len(features)
    )

    X_train = shuffled_features[
        :split_index
    ]

    X_test = shuffled_features[
        split_index:
    ]

    y_train = shuffled_target[
        :split_index
    ]

    y_test = shuffled_target[
        split_index:
    ]

    print("\n" + "=" * 60)
    print("TRAIN / TEST SPLIT")
    print("=" * 60)

    print(
        "\nTraining Features:",
        X_train.shape
    )

    print(
        "Testing Features :",
        X_test.shape
    )

    print(
        "Training Target  :",
        y_train.shape
    )

    print(
        "Testing Target   :",
        y_test.shape
    )


# ============================================================
# 10. MATRIX OPERATIONS
# ============================================================

def matrix_operations():

    print("\n" + "=" * 60)
    print("MATRIX OPERATIONS")
    print("=" * 60)

    A = np.array([
        [1, 2],
        [3, 4]
    ])

    B = np.array([
        [5, 6],
        [7, 8]
    ])

    print("\nMatrix A:")
    print(A)

    print("\nMatrix B:")
    print(B)

    # Transpose

    print("\nTranspose of A:")
    print(A.T)

    # Element-wise multiplication

    print("\nElement-wise multiplication:")
    print(A * B)

    # Dot product

    print("\nDot Product:")
    print(np.dot(A, B))

    # Matrix multiplication

    print("\nMatrix Multiplication:")
    print(np.matmul(A, B))

    # @ operator

    print("\nUsing @ operator:")
    print(A @ B)


# ============================================================
# 11. LINEAR ALGEBRA
# ============================================================

def linear_algebra_analysis():

    print("\n" + "=" * 60)
    print("LINEAR ALGEBRA ANALYSIS")
    print("=" * 60)

    A = np.array([
        [4, 2],
        [1, 3]
    ], dtype=float)

    print("\nMatrix:")
    print(A)

    # Determinant

    determinant = np.linalg.det(A)

    print(
        "\nDeterminant:",
        determinant
    )

    # Inverse

    inverse = np.linalg.inv(A)

    print("\nInverse:")
    print(inverse)

    # Eigenvalues and Eigenvectors

    eigenvalues, eigenvectors = np.linalg.eig(A)

    print("\nEigenvalues:")
    print(eigenvalues)

    print("\nEigenvectors:")
    print(eigenvectors)


# ============================================================
# 12. SAVE PROCESSED DATA
# ============================================================

def save_processed_data():

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    # Save feature matrix

    np.save(
        PROCESSED_FILE,
        features
    )

    print("\nProcessed feature data saved.")

    print(
        "File:",
        PROCESSED_FILE
    )

    # Save train/test if available

    if X_train is not None:

        np.savez(
            "train_test_data.npz",
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test
        )

        print(
            "Train/Test data saved as:",
            "train_test_data.npz"
        )


# ============================================================
# 13. LOAD SAVED DATA
# ============================================================

def load_saved_data():

    print("\n" + "=" * 60)
    print("LOAD SAVED NUMPY DATA")
    print("=" * 60)

    if os.path.exists(PROCESSED_FILE):

        loaded_data = np.load(
            PROCESSED_FILE
        )

        print(
            "\nProcessed data loaded."
        )

        print(
            "Shape:",
            loaded_data.shape
        )

    else:

        print(
            "\nProcessed data file not found."
        )

    if os.path.exists(
        "train_test_data.npz"
    ):

        saved = np.load(
            "train_test_data.npz"
        )

        print(
            "\nTrain/Test data loaded."
        )

        print(
            "X_train:",
            saved["X_train"].shape
        )

        print(
            "X_test:",
            saved["X_test"].shape
        )

        print(
            "y_train:",
            saved["y_train"].shape
        )

        print(
            "y_test:",
            saved["y_test"].shape
        )


# ============================================================
# 14. EXPORT TO CSV
# ============================================================

def export_processed_data():

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    np.savetxt(
        EXPORT_FILE,
        features,
        delimiter=",",
        header=(
            "age,experience,projects,"
            "working_hours,performance_score"
        ),
        comments="",
        fmt="%.4f"
    )

    print("\nProcessed data exported.")

    print(
        "File:",
        EXPORT_FILE
    )


# ============================================================
# 15. VECTORIZATION VS LOOP
# ============================================================

def performance_comparison():

    print("\n" + "=" * 60)
    print("NUMPY PERFORMANCE COMPARISON")
    print("=" * 60)

    np.random.seed(42)

    numbers = np.random.rand(
        1_000_000
    )

    # --------------------------------------------------------
    # Python Loop
    # --------------------------------------------------------

    start = time.perf_counter()

    loop_result = []

    for value in numbers:

        loop_result.append(
            value * 2
        )

    loop_time = (
        time.perf_counter()
        - start
    )

    # --------------------------------------------------------
    # NumPy Vectorization
    # --------------------------------------------------------

    start = time.perf_counter()

    numpy_result = numbers * 2

    numpy_time = (
        time.perf_counter()
        - start
    )

    print(
        f"\nPython Loop Time     : "
        f"{loop_time:.6f} seconds"
    )

    print(
        f"NumPy Vectorized Time: "
        f"{numpy_time:.6f} seconds"
    )

    if numpy_time > 0:

        speedup = (
            loop_time / numpy_time
        )

        print(
            f"\nNumPy Speedup: "
            f"{speedup:.2f}x"
        )

    print(
        "\nVectorized calculation completed."
    )


# ============================================================
# 16. FINAL REPORT
# ============================================================

def final_report():

    if features is None:

        print("\nPlease clean the dataset first.")

        return

    print("\n")
    print("=" * 70)
    print("           ML DATA PREPROCESSING REPORT")
    print("=" * 70)

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    print("\nDATASET")
    print("-" * 70)

    print(
        "Total Records       :",
        len(features)
    )

    print(
        "Number of Features  :",
        features.shape[1]
    )

    print(
        "Feature Matrix Shape:",
        features.shape
    )

    print(
        "Target Shape        :",
        target.shape
    )

    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    print("\nFEATURES")
    print("-" * 70)

    feature_names = [
        "Age",
        "Experience",
        "Projects",
        "Working Hours",
        "Performance Score"
    ]

    for name in feature_names:

        print(
            "-",
            name
        )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    print("\nFEATURE STATISTICS")
    print("-" * 70)

    means = np.mean(
        features,
        axis=0
    )

    stds = np.std(
        features,
        axis=0
    )

    for i in range(
        len(feature_names)
    ):

        print(
            f"{feature_names[i]:<20}"
            f"Mean: {means[i]:>10.2f}   "
            f"Std: {stds[i]:>10.2f}"
        )

    # --------------------------------------------------------
    # Salary
    # --------------------------------------------------------

    print("\nTARGET / SALARY")
    print("-" * 70)

    print(
        f"Average Salary: "
        f"₹{np.mean(target):,.2f}"
    )

    print(
        f"Minimum Salary: "
        f"₹{np.min(target):,.2f}"
    )

    print(
        f"Maximum Salary: "
        f"₹{np.max(target):,.2f}"
    )

    # --------------------------------------------------------
    # Train/Test
    # --------------------------------------------------------

    if X_train is not None:

        print("\nTRAIN / TEST")
        print("-" * 70)

        print(
            "Training Records:",
            len(X_train)
        )

        print(
            "Testing Records :",
            len(X_test)
        )

        print(
            "Training Ratio  : 80%"
        )

        print(
            "Testing Ratio   : 20%"
        )

    # --------------------------------------------------------
    # Scaling
    # --------------------------------------------------------

    print("\nSCALING")
    print("-" * 70)

    print(
        "Normalization    :",
        "Completed"
        if normalized_data is not None
        else "Not performed"
    )

    print(
        "Standardization  :",
        "Completed"
        if standardized_data is not None
        else "Not performed"
    )

    # --------------------------------------------------------
    # Save Status
    # --------------------------------------------------------

    print("\nFILES")
    print("-" * 70)

    print(
        "Processed NumPy File:",
        PROCESSED_FILE
        if os.path.exists(PROCESSED_FILE)
        else "Not created"
    )

    print(
        "Train/Test File:",
        "train_test_data.npz"
        if os.path.exists(
            "train_test_data.npz"
        )
        else "Not created"
    )

    print("\n" + "=" * 70)
    print("              END OF REPORT")
    print("=" * 70)


# ============================================================
# MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")
        print("=" * 65)
        print("        ML DATA PREPROCESSING ENGINE")
        print("=" * 65)

        print("\n1.  Generate Dataset")
        print("2.  Load Dataset")
        print("3.  Dataset Information")
        print("4.  View Data")
        print("5.  Data Quality Check")
        print("6.  Clean Data")
        print("7.  Normalize Features")
        print("8.  Standardize Features")
        print("9.  Train/Test Split")
        print("10. Matrix Operations")
        print("11. Linear Algebra Analysis")
        print("12. Save Processed Data")
        print("13. Load Saved Data")
        print("14. Export Processed CSV")
        print("15. Performance Comparison")
        print("16. Final Report")
        print("0.  Exit")

        choice = input(
            "\nEnter your choice: "
        )

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

            clean_data()

        elif choice == "7":

            normalize_features()

        elif choice == "8":

            standardize_features()

        elif choice == "9":

            train_test_split_data()

        elif choice == "10":

            matrix_operations()

        elif choice == "11":

            linear_algebra_analysis()

        elif choice == "12":

            save_processed_data()

        elif choice == "13":

            load_saved_data()

        elif choice == "14":

            export_processed_data()

        elif choice == "15":

            performance_comparison()

        elif choice == "16":

            final_report()

        elif choice == "0":

            print(
                "\nExiting ML Data Preprocessing Engine..."
            )

            print(
                "Thank you for using the system!"
            )

            break

        else:

            print(
                "\nInvalid choice. Please try again."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()