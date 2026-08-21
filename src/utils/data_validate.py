import great_expectations as gx
import pandas as pd


def validate_telco_data(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate Telco Customer Churn data using Great Expectations 1.x.

    Returns:
        tuple:
            - bool: True if all expectations pass
            - list[str]: Names of failed expectations
    """

    print("🔍 Starting data validation with Great Expectations...")

    # ============================================================
    # Create an ephemeral GE context
    # ============================================================
    context = gx.get_context(mode="ephemeral")

    # ============================================================
    # Create Pandas datasource
    # ============================================================
    datasource = context.data_sources.add_pandas(
        name="telco_pandas_datasource"
    )

    # ============================================================
    # Create dataframe data asset
    # ============================================================
    data_asset = datasource.add_dataframe_asset(
        name="telco_customer_data"
    )

    # ============================================================
    # Create batch definition
    # ============================================================
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "telco_batch"
    )

    # Normalize numeric fields before applying numeric expectations. The raw
    # CSV contains TotalCharges as text because some rows are blank.
    validation_df = df.copy()
    for column in ["tenure", "MonthlyCharges", "TotalCharges"]:
        if column in validation_df.columns:
            validation_df[column] = pd.to_numeric(validation_df[column], errors="coerce")

    # Get the actual batch containing our DataFrame
    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": validation_df}
    )

    # ============================================================
    # Define expectations
    # ============================================================
    expectations = [
        # --------------------------------------------------------
        # Schema validation
        # --------------------------------------------------------

        gx.expectations.ExpectColumnToExist(
            column="customerID"
        ),

        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customerID"
        ),

        gx.expectations.ExpectColumnToExist(
            column="gender"
        ),

        gx.expectations.ExpectColumnToExist(
            column="Partner"
        ),

        gx.expectations.ExpectColumnToExist(
            column="Dependents"
        ),

        gx.expectations.ExpectColumnToExist(
            column="PhoneService"
        ),

        gx.expectations.ExpectColumnToExist(
            column="InternetService"
        ),

        gx.expectations.ExpectColumnToExist(
            column="Contract"
        ),

        gx.expectations.ExpectColumnToExist(
            column="tenure"
        ),

        gx.expectations.ExpectColumnToExist(
            column="MonthlyCharges"
        ),

        gx.expectations.ExpectColumnToExist(
            column="TotalCharges"
        ),

        # --------------------------------------------------------
        # Business logic validation
        # --------------------------------------------------------

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="gender",
            value_set=["Male", "Female"]
        ),

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Partner",
            value_set=["Yes", "No"]
        ),

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Dependents",
            value_set=["Yes", "No"]
        ),

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="PhoneService",
            value_set=["Yes", "No"]
        ),

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Contract",
            value_set=[
                "Month-to-month",
                "One year",
                "Two year"
            ]
        ),

        gx.expectations.ExpectColumnValuesToBeInSet(
            column="InternetService",
            value_set=[
                "DSL",
                "Fiber optic",
                "No"
            ]
        ),

        # --------------------------------------------------------
        # Numeric range validation
        # --------------------------------------------------------

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="tenure",
            min_value=0
        ),

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="MonthlyCharges",
            min_value=0
        ),

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="TotalCharges",
            min_value=0
        ),

        # --------------------------------------------------------
        # Statistical/business constraints
        # --------------------------------------------------------

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="tenure",
            min_value=0,
            max_value=120
        ),

        gx.expectations.ExpectColumnValuesToBeBetween(
            column="MonthlyCharges",
            min_value=0,
            max_value=200
        ),

        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="tenure"
        ),

        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="MonthlyCharges"
        ),

        # --------------------------------------------------------
        # Data consistency
        # --------------------------------------------------------

        gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
            column_A="TotalCharges",
            column_B="MonthlyCharges",
            or_equal=True,
            mostly=0.95
        ),
    ]

    # ============================================================
    # Run validation
    # ============================================================
    print("   ⚙️ Running validation suite...")

    failed_expectations = []

    total_checks = len(expectations)
    passed_checks = 0

    for expectation in expectations:

        result = batch.validate(expectation)

        if result.success:
            passed_checks += 1

        else:
            failed_expectations.append(
                expectation.expectation_type
            )

    failed_checks = total_checks - passed_checks

    # ============================================================
    # Print results
    # ============================================================
    if failed_checks == 0:

        print(
            f"✅ Data validation PASSED: "
            f"{passed_checks}/{total_checks} checks successful"
        )

        return True, []

    print(
        f"❌ Data validation FAILED: "
        f"{failed_checks}/{total_checks} checks failed"
    )

    print(
        f"   Failed expectations: "
        f"{failed_expectations}"
    )

    return False, failed_expectations