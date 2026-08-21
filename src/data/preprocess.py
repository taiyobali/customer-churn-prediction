import pandas as pd

def preprocess_data(df: pd.DataFrame, target_col: str = "Churn") -> pd.DataFrame:
    """
    Basic cleaning for Telco Churn
    - trim column names
    - drop obvious ID cols
    - fix TotalCharges to numeric
    - map target Churn to 0/1 if needed
    - simple NA handling
    """
    #tidy headers
    df.columns =  df.columns.str.strip() #remove whitespace

    #drop ids if present
    for col in ["customerID", "CustomerID", "customer_id"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    #target to 0/1 if it's Yes/No
    if target_col in df.columns and df[target_col].dtype =="object":
        values = df[target_col].dropna().astype(str).str.strip()

        invalid = set(values) - {"Yes", "No"}

        if invalid:
            raise ValueError(f"Invalid Values in {target_col}: {invalid}")
        
        df[target_col] = values.map({"Yes":1, "No":0})

    #TotalCharges often has blanks
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    #SeniorCitizen should be 0/1 int if present
    if "SeniorCitizen" in df.columns:
        df["SeniorCitizen"] = df["SeniorCitizen"].fillna(0).astype(int)

    #simple NA strategy
    # - numeric fill with 0
    # - others: for for encoders to handle 

    num_cols = df.select_dtypes(include=["number"]).columns 
    df[num_cols] = df[num_cols].fillna(0)

    return df 






