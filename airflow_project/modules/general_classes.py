import json
import os
import pandas as pd

def save_csv(df,file):
    if os.path.exists(file):
        saved_df = pd.read_csv(os.path.join(file), on_bad_lines='skip').drop_duplicates() #Open file
        frames = [df, saved_df]
        df_final = pd.concat(frames)
        df_final.to_csv(os.path.join(file), encoding='utf-8-sig',index=False)
    else:
        df.to_csv(os.path.join(file), encoding='utf-8-sig',index=False)


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
        with open(saved_json_path, 'r',  encoding="UTF-8") as f:
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

            unique_dicts = [d for d in new_json_data if d not in saved_data]
            saved_data.extend(unique_dicts)
            with open(saved_json_path, 'w', encoding="UTF-8") as file:
                json.dump(saved_data, file, indent=4, ensure_ascii=False)
        else:
            with open(saved_json_path, 'w', encoding="UTF-8") as file:
                json.dump(new_json_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print("save_merge_json - Error occurs: ", str(e))