from types import SimpleNamespace
import json
import os
import pandas as pd
# using numpy
import numpy as np

def save_csv(df,file):
    if os.path.exists(os.path.join('./data/craw', file)):
        saved_df = pd.read_csv(os.path.join('./data/craw', file), on_bad_lines='skip').drop_duplicates() #Open file
        frames = [df, saved_df]
        df_final = pd.concat(frames)
        df_final.to_csv(os.path.join('./data/craw', file), encoding='utf-8-sig',index=False)
    else:
        df.to_csv(os.path.join('./data/craw', file), encoding='utf-8-sig',index=False)


def save_json(new_json_data, uri_path):
    try:
        # Đọc dữ liệu từ tệp JSON cũ nếu tệp tồn tại
        saved_json_path = os.path.join(uri_path)
        if os.path.exists(saved_json_path):
            os.remove(saved_json_path)
            print(f"Removed {saved_json_path}")
        with open(saved_json_path, "w", encoding='utf-8') as data:
            json.dump(new_json_data, data, ensure_ascii=False)
        print(f"Saved success: {saved_json_path}")
    except Exception as e:
        print("Đã xảy ra lỗi:", str(e))

def read_json(uri_path):
    saved_json_path = os.path.join(uri_path)
    if os.path.exists(saved_json_path):
        with open(saved_json_path, 'r') as f:
            data = json.load(f)
            return data
    else:
        return None

def save_merge_json(new_json_data, uri_path):
    try:
        # Đọc dữ liệu từ tệp JSON cũ nếu tệp tồn tại
        saved_json_path = os.path.join(uri_path)
        if os.path.exists(saved_json_path):
            with open(saved_json_path, 'r', encoding="UTF-8") as file:
                saved_data = json.load(file)

            saved_data.extend(new_json_data)
            with open(saved_json_path, 'w', encoding="UTF-8") as file:
                json.dump(saved_data, file, indent=4, ensure_ascii=False)
        else:
            with open(saved_json_path, 'w', encoding="UTF-8") as file:
                json.dump(new_json_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Error occurs: ", str(e))

