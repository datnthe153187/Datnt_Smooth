df_vn30 = get_data_vn30(1000)
df_vn30 = r(df_vn30, 1, 'D')
df_vn30.Date = pd.to_datetime(df_vn30.Date)
df_vn30.to_csv('/Users/phamhuy/Documents/GitHub/quant-trading-result/df_vn30.csv', index=False)
df_vn30 
