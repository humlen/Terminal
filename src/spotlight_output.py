"""
Writes Lantern data to Excel
"""
import pandas as pd 

# Variables
link_pb = "C:/Users/eirik/Codebase/Reports/PowerBI Resources"

# Write to Excel
def lantern_writer(df_is,df_bs,df_cf,df_kr,df_fd,df_pd):
    with pd.ExcelWriter(f'{link_pb}/BDR.xlsx') as writer: # type: ignore
        df_pd.to_excel(writer, sheet_name='Price Data', index = False)

        try:
            df_fd.to_excel(writer, sheet_name='Info', index = False)

        except Exception: 
            pass

        df_is.to_excel(writer, sheet_name='Income Statement', index = False)
        df_bs.to_excel(writer, sheet_name='Balance Sheet', index = False)
        df_cf.to_excel(writer, sheet_name='Cash Flow Statement', index = False)
        df_kr.to_excel(writer, sheet_name = "Key Ratios", index = False)

