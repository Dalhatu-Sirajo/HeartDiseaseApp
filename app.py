import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Heart Disease App", layout="wide")

st.title("💓 Heart Disease Analysis")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("cleve.csv")

df = load_data()

st.sidebar.header("🔎 Filter Data")

# Mappings
gender_map = {0: 'Female', 1: 'Male'}
cp_map = {
    1: 'Typical Angina',
    2: 'Atypical Angina',
    3: 'Non-anginal Pain',
    4: 'Asymptomatic'
}

df['sex'] = df['sex'].map(gender_map)
df['cp'] = df['cp'].map(cp_map)

selected_gender = st.sidebar.selectbox("Select Gender", options=["All"] + df["sex"].unique().tolist())
selected_cp = st.sidebar.selectbox("Chest Pain Type", options=["All"] + df["cp"].unique().tolist())

trestbps_min, trestbps_max = st.sidebar.slider(
    "Resting BP Range (trestbps)", 
    int(df["trestbps"].min()), 
    int(df["trestbps"].max()), 
    (100, 140)
)

selected_cols = st.sidebar.multiselect(
    "📑 Columns to Display", 
    df.columns.tolist(), 
    default=["age", "sex", "cp", "chol", "num"]
)

# Apply filters
filtered_df = df.copy()
if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["sex"] == selected_gender]
if selected_cp != "All":
    filtered_df = filtered_df[filtered_df["cp"] == selected_cp]

filtered_df = filtered_df[
    (filtered_df["trestbps"] >= trestbps_min) & (filtered_df["trestbps"] <= trestbps_max)
]

# Show preview
st.subheader("📊 Filtered Dataset Preview")
st.dataframe(filtered_df[selected_cols])

# Summary statistics
if st.sidebar.checkbox("Show Summary Statistics"):
    st.subheader("📈 Summary Statistics")
    st.write(filtered_df.describe())

# Choose a chart
chart = st.sidebar.selectbox(
    "📌 Choose Visualization",
    ["None", "Age vs Cholesterol", "Heart Disease Count", "Correlation Heatmap", "Custom Scatter Plot"]
)

if chart == "Age vs Cholesterol":
    st.subheader("🧠 Age vs Cholesterol by Heart Disease")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(data=filtered_df, x="age", y="chol", hue="num", ax=ax1)
    st.pyplot(fig1)

elif chart == "Heart Disease Count":
    st.subheader("❤️ Heart Disease Outcome Count")
    fig2, ax2 = plt.subplots()
    sns.countplot(data=filtered_df, x="num", hue="sex", ax=ax2)
    ax2.set_xticklabels(["No Disease", "Disease"])
    st.pyplot(fig2)

elif chart == "Correlation Heatmap":
    st.subheader("🔗 Correlation Heatmap")
    
    df_encoded = filtered_df.copy()
    df_encoded['sex'] = df_encoded['sex'].map({'Male': 1, 'Female': 0})
    df_encoded['cp'] = df_encoded['cp'].map({'Typical Angina': 1, 'Atypical Angina': 2, 'Non-anginal Pain': 3, 'Asymptomatic': 4})
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_encoded[selected_cols].corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

elif chart == "Custom Scatter Plot":
    st.subheader("📌 Custom Scatter Plot")
    x_axis = st.selectbox("Select X-axis", df.columns)
    y_axis = st.selectbox("Select Y-axis", df.columns)
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, hue="num", ax=ax4)
    ax4.set_title(f"{y_axis} vs {x_axis} colored by Heart Disease")
    st.pyplot(fig4)

st.markdown("---")
st.markdown("👨🏽‍💻 Developed by **SMD**")
