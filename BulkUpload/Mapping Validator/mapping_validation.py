import pandas as pd
import json
myntraMappedData = pd.read_excel("Flipkart Mapping.xlsx")

master_data=json.load(open('../catalog-full.json'))['result']

def filter_data_by_categories(super_category, category, sub_category, sub_sub_category):
    filtered_data = [
        item["sub_sub_category_id"]
        for item in master_data
        if item["super_category"] == super_category
        and item["category"] == category
        and item["sub_category"] == sub_category
        and item["sub_sub_category"] == sub_sub_category
    ]
    return filtered_data[0] if len(filtered_data)>0 else "invalid mapping"

for index, row in myntraMappedData.iterrows():
    id=filter_data_by_categories(row["Super cateogry"],row["Category"],row["Sub Category"],row["Product type"])
    myntraMappedData.at[index, "sub_sub_category_id"] = id
myntraMappedData.to_excel("flipkartMappedValidation.xlsx")