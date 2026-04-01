import streamlit as st 
import numpy as np 
import pandas as pd
import datetime

st.title("DatNT_Smooth")
sidebar_radiio = st.sidebar.radio(
    'Chức Năng', 
    ("Kết quả đầu tư", "Tính lợi nhuận")
)

def plot_pnl(): 
    df = pd.read_csv('pnl_live.csv')
    df.Date = pd.to_datetime(df.Date)
    df.Date = df.Date.dt.date
    arr_gain = df.gain.values 
    

    df['total_gain_new'] = (df.gain + 1).cumprod() * 100
    # df['total_gain_new'] = df['total_gain_new']
    total_gain_today = str(np.round((df.total_gain_new.values[-1]), 2))
    gain_today =  str(np.round(arr_gain[-1] * 100, 2))
    
    df_vn30 = pd.read_csv('df_vn30.csv')


    df_vn30.Date = pd.to_datetime(df_vn30.Date)
    # df_vn30.Date = df_vn30.Date.dt.date

    df_vn30 = df_vn30[df_vn30.Date.isin(df.Date)].dropna()
    # df_vn30['gain'] = df_vn30.Close.diff()
    df_vn30['gain'] = (df_vn30['Close']/df_vn30['Close'].shift(1)-1)
    vn30_gain = df_vn30.gain.values 

    df_vn30['total_gain_new'] = (df_vn30.gain + 1).cumprod() * 100
    # df_vn30['total'] = df_vn30['gain'].cumsum()
    # df_vn30.gain = (df_vn30.gain/df_vn30.Close.shift(1)).values * 100 
    # df_vn30['gain'].iloc[0] = 0
    # df_vn30['total_gain'] = df_vn30.gain.cumsum()
    
    chart_data = pd.DataFrame()
    chart_data['Date'] = pd.to_datetime(df.Date)
    print(len(chart_data))
    print(len(df_vn30))
    # chart_data['VN30'] = df_vn30['total_gain_new'].values 
    chart_data['VN30'] = df_vn30['total_gain_new']
    chart_data['Kết quả đầu tư'] = df['total_gain_new'].values 
    
    col1, col2 = st.columns(2)
    with col1: 
        st.metric(label="Kết quả đầu tư của tôi", value=total_gain_today, delta=gain_today + '%')
    with col2: 
        st.metric(label="Tăng trưởng của VN30", value=str(np.round(df_vn30.total_gain_new.iloc[-1], 2)), delta=str(np.round(df_vn30.gain.iloc[-1] * 100, 2)) + ' %')

    st.line_chart(chart_data, x="Date", y=["VN30", "Kết quả đầu tư"])
    st.caption('Kết quả đầu tư so với tăng trưởng của VN30')
    
    # so sanh
    sharpe_alpha = df['gain'].mean()/ df['gain'].std() * np.sqrt(252)
    mdd_alpha = -(chart_data['Kết quả đầu tư']/chart_data['Kết quả đầu tư'].cummax() - 1).min() 

    sharpe_vn30 = df_vn30['gain'].mean()/ df_vn30['gain'].std() * np.sqrt(252)
    mdd_vn30 = -(chart_data['VN30']/chart_data['VN30'].cummax() - 1).min() 
    
    comparison_data = {
        'Chỉ số': [
            'Sharpe Ratio',
            'Sụt giảm lớn nhất',
        ],
        'DatNT_Smooth': [
            f"{np.round(sharpe_alpha, 2)}",
            f"{np.round(mdd_alpha * 100, 2)}%"
        ],
        'VN30': [
            f"{np.round(sharpe_vn30, 2)}",
            f"{np.round(mdd_vn30 * 100, 2)}%"
        ]
    }
    st.dataframe(
    comparison_data,
    use_container_width=True,
    hide_index=True
    )
    # r_w_alpha = chart_data['Kết quả đầu tư'].iloc[-1]/chart_data['Kết quả đầu tư'].iloc[-6] - 1 
    # r_m_alpha = chart_data['Kết quả đầu tư'].iloc[-1]/chart_data['Kết quả đầu tư'].iloc[-22] - 1 
    # r_q_alpha = chart_data['Kết quả đầu tư'].iloc[-1]/chart_data['Kết quả đầu tư'].iloc[-64] - 1 
    # r_y_alpha = chart_data['Kết quả đầu tư'].iloc[-1]/chart_data['Kết quả đầu tư'].iloc[-253] - 1 
    # r_all_alpha = chart_data['Kết quả đầu tư'].iloc[-1]/chart_data['Kết quả đầu tư'][0] - 1 
    
    # r_w_vn30 = chart_data['VN30'].iloc[-1]/chart_data['VN30'].iloc[-6] - 1 
    # r_m_vn30 = chart_data['VN30'].iloc[-1]/chart_data['VN30'].iloc[-22] - 1 
    # r_q_vn30 = chart_data['VN30'].iloc[-1]/chart_data['VN30'].iloc[-64] - 1 
    # r_y_vn30 = chart_data['VN30'].iloc[-1]/chart_data['VN30'].iloc[-253] - 1 
    # r_all_vn30 = chart_data['VN30'].iloc[-1]/100 - 1 

    # return_data = {
    #     'Lợi nhuận (%)': [
    #         '5 phiên gần nhất (1 tuần)',
    #         '21 phiên gần nhất (1 tháng)',
    #         '63 phiên gần nhất (1 quý)',
    #         '252 phiên gần nhất (1 năm)',
    #         'Từ ngày bắt đầu',

    #     ],
    #     'DatNT_Smooth': [
    #         f"{np.round(r_w_alpha * 100, 2)}%",
    #         f"{np.round(r_m_alpha * 100, 2)}%",
    #         f"{np.round(r_q_alpha * 100, 2)}%",
    #         f"{np.round(r_y_alpha * 100, 2)}%",
    #         f"{np.round(r_all_alpha * 100, 2)}%"

    #     ],
    #     'VN30': [
    #         f"{np.round(r_w_vn30 * 100, 2)}%",
    #         f"{np.round(r_m_vn30 * 100, 2)}%",
    #         f"{np.round(r_q_vn30 * 100, 2)}%",
    #         f"{np.round(r_y_vn30 * 100, 2)}%",
    #         f"{np.round(r_all_vn30 * 100, 2)}%"
    #     ]
    # }
    # st.dataframe(
    # return_data,
    # use_container_width=True,
    # hide_index=True
    # )

def calculate_profit():
    st.title("Tính Lợi Nhuận")

    start_day = st.date_input("Ngày bắt đầu", datetime.date(2026, 1, 1))
    start_end = st.date_input("Ngày tất toán", datetime.date.today())
    start_day = pd.to_datetime(start_day)
    start_end = pd.to_datetime(start_end)
    total_money = st.number_input("Số tiền đầu tư (triệu đ): ", 0)

    df = pd.read_csv('pnl_live.csv')
    df.Date = pd.to_datetime(df.Date)
    date_range = pd.date_range(start=start_day, end=start_end, freq='D')  
    number_of_days = len(date_range)
    df['total_gain_new'] = (df.gain + 1).cumprod() 

    filtered_df = df[(df['Date'] >= start_day) & (df['Date'] <= start_end)]
    out_df = df[(df['Date'] < start_day) ]
    # arr_gain = filtered_df.gain.values 
    # number_of_days = len(filtered_df)
    # arr_gain = filtered_df.gain.values       
    
    # arr_total_new = np.zeros(len(filtered_df))
    
    # filtered_df['total_gain_new'] = (filtered_df.gain + 1).cumprod() 
    # out_df['total_gain_new'] = (out_df.gain + 1).cumprod() 

    # total_gain = np.sum(arr_gain)
    total_gain = filtered_df['total_gain_new'].iloc[-1]/out_df['total_gain_new'].iloc[-1] - 1
    gain_per_year  = (total_gain/number_of_days) * 365

    Tong_tien = str(np.round((1 + total_gain) * total_money , 2)) + " triệu đ"
    Lai =  str(np.round(total_gain * total_money, 2)) + " triệu đ"
    Tong_lai = total_gain * total_money
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tổng tiền", value= Tong_tien, delta=Lai)
        Gain_yearly = str(np.round(gain_per_year * 100, 2)) + '%'
        st.metric(label="Hiệu suất đầu tư trung bình/ năm", value= Gain_yearly)

    # st.subheader("Tỷ Lệ Phân Bổ")

    # option = st.radio(
    #     "Chọn phương án phân bổ:",
    #     ("Option 1: 80-20")
    # )

    st.markdown("### Kết quả phân bổ")
    if gain_per_year >= 0: 
        # if option == "Option 1: 80-20":
            # st.success("✅ Bạn đã chọn Option 2 với tỷ lệ 80-20.")
            print('lãi')
            st.caption("Hiệu suất dưới 50%, bạn sẽ nhận 80%, từ phần trăm thứ 51 tôi sẽ nhận 80%")
            if gain_per_year < 0.5: 
                # return_final = np.round(total_gain * total_money * 0.8, 2)
                st.write(f"Lãi thu về: {np.round(Tong_lai * 0.8)} triệu đ")
            else: 
                return_final = np.round(Tong_lai * (0.3/gain_per_year + 0.2), 2)   
                st.write(f"Lãi thu về: {return_final} triệu đ")
    else: 
        # st.success("✅ Bạn đã chọn Option 1 với tỷ lệ 50-50.")
        print('lỗ')
        return_final = np.round(total_gain * total_money, 2)
        st.write(f"Lãi thu về: {return_final} triệu đ")
login = True 
if login == True: 
    if sidebar_radiio == "Kết quả đầu tư": 
        plot_pnl()
    elif sidebar_radiio == 'Tính lợi nhuận': 
        calculate_profit()