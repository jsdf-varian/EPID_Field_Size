import glob
import pandas as pd
from datetime import datetime

from run import main

def export_csv(file_name=None):
    if file_name is None:
        file_name = datetime.now().strftime("%Y-%m%d-%H%M")
        
    pattern = "files/*/*.dcm"
    files = glob.glob(pattern)
    field_list = []
    print("="*50)
    for file in files:
        field_dict = {}
        print(f"{file}")
        size = file.split(".dcm")[0][-4:]
        inline, crossline = main(file, figure=False)
        field_dict["field_size"] = size
        field_dict["In-line"] = round(inline, ndigits=2)
        field_dict["Cross-line"] = round(crossline, ndigits=2)
        field_list.append(field_dict)
        print("="*50)
    pd.DataFrame(field_list).to_csv(f"results/{file_name}.csv")