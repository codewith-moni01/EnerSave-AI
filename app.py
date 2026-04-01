import streamlit as st
import pandas as pd
import numpy as np

# ------------------ SESSION ------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------ LOGIN / SIGNUP ------------------
def login_signup():
    st.title("🔐 EnerSave AI Login")

    option = st.radio("Choose Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Login":
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    else:
        if st.button("Signup"):
            if username in st.session_state.users:
                st.warning("User already exists ⚠️")
            else:
                st.session_state.users[username] = password
                st.success("Account created ✅ Please login")

# Stop if not logged in
if not st.session_state.logged_in:
    login_signup()
    st.stop()

# ------------------ MAIN APP ------------------
st.set_page_config(page_title="EnerSave AI", layout="wide")

st.title("⚡ EnerSave AI – Smart Energy Assistant")
st.sidebar.success(f"Welcome {st.session_state.username} 👋")

# ------------------ INPUTS ------------------
col1, col2 = st.columns(2)

with col1:
    temperature = st.slider("🌡 Temperature", 15, 45, 25)

with col2:
    household = st.slider("🏠 Household Size", 1, 10, 4)

# ------------------ PREDICTION (Dummy Model) ------------------
units = (temperature * 2) + (household * 15)
bill = units * 8
carbon = units * 0.82

# ------------------ RESULTS ------------------
st.subheader("📊 Results")

col1, col2, col3 = st.columns(3)

col1.metric("⚡ Units", round(units, 2))
col2.metric("💰 Bill (₹)", round(bill, 2))
col3.metric("🌱 CO₂ (kg)", round(carbon, 2))

# ------------------ ENERGY SCORE ------------------
score = max(10 - (units / 50), 1)
st.subheader(f"⚡ Energy Score: {round(score,1)} / 10")

# ------------------ SMART RECOMMENDATIONS ------------------
st.subheader("💡 Smart Recommendations")

if units > 150:
    st.warning("⚠️ High energy usage detected")

    st.write("👉 Reduce AC usage by 2 hours → Save ₹200")
    st.write("👉 Switch to LED bulbs → Save ₹100")
    st.write("👉 Turn off idle appliances")

else:
    st.success("✅ Your energy usage is efficient!")

# ------------------ GRAPH ------------------
st.subheader("📈 Usage Visualization")

data = pd.DataFrame({
    "Days": range(1, 8),
    "Units": np.random.randint(50, int(units), 7)
})

st.line_chart(data.set_index("Days"))

# ------------------ CHATBOT ------------------
st.subheader("🤖 AI Chatbot")

user_input = st.text_input("Ask something...")

def chatbot_response(text):
    text = text.lower()

    if "reduce" in text:
        return "Use energy-efficient appliances and reduce AC usage."
    elif "bill" in text:
        return f"Your estimated bill is ₹{round(bill,2)}."
    elif "save" in text:
        return "Switch to LED and avoid standby power usage."
    else:
        return "I can help you save energy! Ask me how 😊"

if user_input:
    st.write("🤖:", chatbot_response(user_input))