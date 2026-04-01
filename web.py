import streamlit as st 
import numpy as np 
import pandas as pd
import datetime

st.title("DatNT_Smooth")

sidebar_radiio = st.sidebar.radio(
    'Chức Năng', 
    ("Kết quả đầu tư", "Tính lợi nhuận")
)

# =========================
# 📊 PLOT PNL
# =========================
def plot_pnl(): 
    # --- Load data ---
    df = pd.read_csv('pnl_live.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    df_vn30 = pd.read_csv('df_vn30.csv')
    df_vn30['Date'] = pd.to_datetime(df_vn30['Date'])

    # --- Tính gain ---
    df['total_gain_new'] = (df['gain'] + 1).cumprod()
    total_gain_today = str(np.round(df['total_gain_new'].iloc[-1] * 100, 2))
    gain_today = str(np.round(df['gain'].iloc[-1] * 100, 2))

    df_vn30['gain'] = df_vn30['Close'] / df_vn30['Close'].shift(1) - 1
    df_vn30['total_gain_new'] = (df_vn30['gain'] + 1).cumprod()

    # --- Merge theo Date ---
    chart_data = df[['Date', 'total_gain_new']].rename(
        columns={'total_gain_new': 'Kết quả đầu tư'}
    )

    df_vn30_plot = df_vn30[['Date', 'total_gain_new']].rename(
        columns={'total_gain_new': 'VN30'}
    )

    chart_data = chart_data.merge(df_vn30_plot, on='Date', how='inner')

    # --- Normalize về cùng gốc 100 🔥 ---
    chart_data['Kết quả đầu tư'] = chart_data['Kết quả đầu tư'] / chart_data['Kết quả đầu tư'].iloc[0] * 100
    chart_data['VN30'] = chart_data['VN30'] / chart_data['VN30'].iloc[0] * 100

    # --- Metrics ---
    col1, col2 = st.columns(2)

    with col1: 
        st.metric(
            label="Kết quả đầu tư của tôi", 
            value=str(np.round(chart_data['Kết quả đầu tư'].iloc[-1], 2)), 
            delta=gain_today + '%'
        )

    with col2: 
        st.metric(
            label="Tăng trưởng của VN30", 
            value=str(np.round(chart_data['VN30'].iloc[-1], 2)), 
            delta=str(np.round(df_vn30['gain'].iloc[-1] * 100, 2)) + ' %'
        )

    # --- Chart ---
    st.line_chart(chart_data, x="Date", y=["VN30", "Kết quả đầu tư"])
    st.caption('Kết quả đầu tư so với tăng trưởng của VN30 (base = 100)')

    # --- Risk metrics ---
    sharpe_alpha = df['gain'].mean() / df['gain'].std() * np.sqrt(252)
    sharpe_vn30 = df_vn30['gain'].mean() / df_vn30['gain'].std() * np.sqrt(252)

    mdd_alpha = -(chart_data['Kết quả đầu tư'] / chart_data['Kết quả đầu tư'].cummax() - 1).min()
    mdd_vn30 = -(chart_data['VN30'] / chart_data['VN30'].cummax() - 1).min()

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

    st.dataframe(comparison_data, use_container_width=True, hide_index=True)


# =========================
# 💰 CALCULATE PROFIT
# =========================
def calculate_profit():
    st.title("Tính Lợi Nhuận")

    start_day = st.date_input("Ngày bắt đầu", datetime.date(2026, 1, 1))
    start_end = st.date_input("Ngày tất toán", datetime.date.today())
    total_money = st.number_input("Số tiền đầu tư (triệu đ): ", 0)

    start_day = pd.to_datetime(start_day)
    start_end = pd.to_datetime(start_end)

    df = pd.read_csv('pnl_live.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    df['total_gain_new'] = (df['gain'] + 1).cumprod()

    filtered_df = df[(df['Date'] >= start_day) & (df['Date'] <= start_end)]
    out_df = df[df['Date'] < start_day]

    if len(filtered_df) == 0 or len(out_df) == 0:
        st.error("Không đủ dữ liệu để tính toán")
        return

    number_of_days = (start_end - start_day).days + 1

    total_gain = filtered_df['total_gain_new'].iloc[-1] / out_df['total_gain_new'].iloc[-1] - 1
    gain_per_year = (total_gain / number_of_days) * 365

    Tong_tien = str(np.round((1 + total_gain) * total_money, 2)) + " triệu đ"
    Lai = str(np.round(total_gain * total_money, 2)) + " triệu đ"
    Tong_lai = total_gain * total_money

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Tổng tiền", value=Tong_tien, delta=Lai)
        st.metric(label="Hiệu suất đầu tư trung bình/ năm", value=str(np.round(gain_per_year * 100, 2)) + '%')

    st.markdown("### Kết quả phân bổ")

    if gain_per_year >= 0: 
        st.caption("Hiệu suất dưới 50%, bạn sẽ nhận 80%, từ phần trăm thứ 51 tôi sẽ nhận 80%")

        if gain_per_year < 0.5: 
            st.write(f"Lãi thu về: {np.round(Tong_lai * 0.8, 2)} triệu đ")
        else: 
            return_final = np.round(Tong_lai * (0.3 / gain_per_year + 0.2), 2)   
            st.write(f"Lãi thu về: {return_final} triệu đ")
    else: 
        st.write(f"Lãi thu về: {np.round(Tong_lai, 2)} triệu đ")


# =========================
# 🚀 MAIN
# =========================
login = True 

if login: 
    if sidebar_radiio == "Kết quả đầu tư": 
        plot_pnl()
    elif sidebar_radiio == 'Tính lợi nhuận': 
        calculate_profit()