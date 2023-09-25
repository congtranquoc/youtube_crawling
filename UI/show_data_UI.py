import tkinter as tk
from tkinter import *
from tkinter import ttk
from mongodb.GetDatabaseFromMongo import *

# Hàm để tạo Treeview cho một tab
def create_tab_treeview_with_data(tab, data):
    # Tạo Treeview cho tab
    tree = ttk.Treeview(tab,show='headings')
    tree["columns"] = ["video_title", "like_count", "view_count", "comment_count"]

    # Thiết lập tiêu đề cho các cột
    tree.heading("video_title", text="Tiêu đề video")
    tree.heading("like_count", text="Lượt thích")
    tree.heading("view_count", text="Lượt xem")
    tree.heading("comment_count", text="Lượt nhận xét")

    # Thêm dữ liệu vào Treeview
    for index, row in data.iterrows():
        tree.insert("", index, values=(row["video_title"], row["like_count"], row["view_count"], row["comment_count"]))
        # Center giá trị của cột
        tree.column("like_count", anchor="center")
        tree.column("view_count", anchor="center")
        tree.column("comment_count", anchor="center")
        # Set width của các cột
        tree.column("video_title", width=500)
        tree.column("like_count", width=100)
        tree.column("view_count", width=100)
        tree.column("comment_count", width=100)

    tree.pack_propagate(0)
    # Tạo các biến để lưu trữ tổng số video, tổng lượt thích, tổng lượt xem
    tab_video_count = 0
    tab_like_count = 0
    tab_view_count = 0
    tab_comment_count = 0

    # Cập nhật các biến này khi duyệt qua DataFrame
    for index, row in data.iterrows():
        try:
            tab_video_count += 1
            tab_like_count += int(row["like_count"])
            tab_view_count += int(row["view_count"])
            tab_comment_count += int(row["comment_count"])
        except ValueError:
            pass

    # Thêm các nhãn để hiển thị các tổng số này trong tab
    label_video_count = ttk.Label(tab, text="Tổng số video: {}".format(tab_video_count))
    label_video_count.pack(pady=(20, 0))
    label_like_count = ttk.Label(tab, text=f"Tổng số lượt thích: {tab_like_count:,}")
    label_like_count.pack(pady=(10, 0))
    label_view_count = ttk.Label(tab, text=f"Tổng số lượt xem: {tab_view_count:,}")
    label_view_count.pack(pady=(10, 0))
    label_comment_count = ttk.Label(tab, text=f"Tổng số nhận xét: {tab_comment_count:,}")
    label_comment_count.pack(pady=(10, 20))

    tree.pack(fill="both", expand=True)

# Hàm để load dữ liệu
def load_data():
    # Chọn bộ sưu tập thứ nhất
    collection1 = db.videoids

    # Chuyển dữ liệu từ collection1 thành một danh sách
    data1 = list(collection1.find())

    # Chọn bộ sưu tập thứ hai
    collection2 = db.statics

    # Chuyển dữ liệu từ collection2 thành một danh sách
    data2 = list(collection2.find())

    # Tạo DataFrame từ danh sách dữ liệu
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    # Ghép dữ liệu từ 2 file jsons
    data = pd.merge(df1, df2, how="inner", on="video_id")


    # Chọn chỉ một số cột cụ thể từ DataFrame
    selected_columns = ["video_title", "like_count", "view_count","comment_count", "playlist_program_y"]

    # Lấy DataFrame với chỉ các cột đã chọn
    data = data[selected_columns]

    return data

# Hàm để tạo và hiển thị tab
def create_tabs(data):
    window = tk.Tk()
    window.title("Phân loại dữ liệu từ MongoDB")
    # Set width
    window.geometry("1200x700")
    # window.attributes("-fullscreen", True)

    # Thiết lập phông chữ Roboto cho tất cả các widget
    window.option_add("*Font", "Roboto")

    # Style
    style = ttk.Style()
    style.configure('TNotebook', tabposition='n', tabmargins=[10, 15, 0, 0])
    style.configure('TNotebook.Tab', background='#d9ffcc', padding=[10, 5])

    # Tạo một đối tượng Notebook để chứa tab
    notebook = ttk.Notebook(window)

    # Tạo tab "Rap Việt" và thêm dữ liệu vào Treeview
    tab1 = ttk.Frame(notebook, width=90, height=40)
    notebook.add(tab1, text="Rap Việt")
    create_tab_treeview_with_data(tab1, data[data["playlist_program_y"] == "videoids_rapvie"])

    # Tạo tab "NALA" và thêm dữ liệu vào Treeview
    tab2 = ttk.Frame(notebook, width=90, height=40)
    notebook.add(tab2, text="Người Ấy Là Ai?")
    create_tab_treeview_with_data(tab2, data[data["playlist_program_y"] == "videoids_nala"])

    notebook.pack(fill="both", expand=True, anchor=CENTER)
    window.mainloop()

# Gọi hàm để tạo và hiển thị tab

data = load_data()
create_tabs(data)
