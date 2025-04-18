import io
import pandas as pd
import streamlit as st
from datetime import datetime

# Load the attendance log
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("attendance_log.csv")
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df
    except FileNotFoundError:
        st.warning("📂 attendance_log.csv not found!")
        return pd.DataFrame(columns=["Name", "Timestamp", "Status"])

df = load_data()

# Title
st.title("🎓 Voice Attendance Dashboard")

# Filters
names = df["Name"].unique().tolist()
names.sort()

selected_name = st.selectbox("🔍 Filter by Name", ["All"] + names)
if selected_name != "All":
    df = df[df["Name"] == selected_name]

selected_date = st.date_input("📅 Filter by Date", value=datetime.today())
df = df[df["Timestamp"].dt.date == selected_date]

# Display
st.subheader("📋 Attendance Records")
st.dataframe(df, use_container_width=True)

# Stats
present_count = df[df["Status"] == "Present"].shape[0]
proxy_count = df[df["Status"] != "Present"].shape[0]

st.markdown("### 📊 Summary")
st.write(f"✅ Present: {present_count}")
st.write(f"❌ Proxy Attempts: {proxy_count}")

# 📁 Download as Excel
st.markdown("### 📥 Download Attendance Log")

if not df.empty:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
        # Save the file (we don’t use writer.save(), it’s automatic)
        writer.close()
        processed_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Excel File",
        data=processed_data,
        file_name='attendance_log.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.info("No attendance records to download.")
