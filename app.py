import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import page1
import page2
import page3
import page4
import warnings
warnings.filterwarnings("ignore")

# Set page configuration at the top
st.set_page_config(page_title="Stock Dashboard", layout="wide")

with open('./config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def save_configfile():
    # Saving config file
    with open('./config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)

def add_black_background_and_banner():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: black;
        }}
        .banner {{
            width: 100%;
            background-color: #59616e;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 24px;
            font-weight: bold;
        }}
        </style>
        <div class="banner">
            Welcome to the Stock Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Initialize session state for reset password and registration
    if 'reset_password' not in st.session_state:
        st.session_state.reset_password = False
    if 'register' not in st.session_state:
        st.session_state.register = False

    # Add black background and banner to the login and registration screens
    add_black_background_and_banner()

    # Toggle between login and registration
    if st.session_state.register:
        st.title("Register User")
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                st.session_state.register = False
                save_configfile()
                st.experimental_rerun()
        except Exception as e:
            st.error(e)
        if st.button("Back to Login"):
            st.session_state.register = False
            st.experimental_rerun()
    else:
        name, authentication_status, username = authenticator.login()

        if authentication_status:
            st.session_state['authentication_status'] = True
            st.session_state['username'] = username
        else:
            st.session_state['authentication_status'] = False

        if st.session_state["authentication_status"]:
            authenticator.logout('Logout', 'sidebar')
            if st.sidebar.button("Reset Password"):
                st.session_state.reset_password = True

            if st.session_state.reset_password:
                st.title("Reset Password")
                try:
                    result = authenticator.reset_password(st.session_state["username"])
                    if result:
                        st.success('Password modified successfully')
                        st.session_state.reset_password = False
                        save_configfile()
                        st.experimental_rerun()
                except Exception as e:
                    st.error(e)
            else:
                st.title(f"Welcome {name}")

                # Sidebar for page navigation
                page = st.sidebar.selectbox("Select a Page", ["Stock Dashboard", "Price Chart", "US & European Stock Indices", "Nifty 50 Stock Scanner"])

                if page == "Stock Dashboard":
                    page1.display_page()
                elif page == "Price Chart":
                    page2.display_page()
                elif page == "US & European Stock Indices":
                    page3.display_page()
                elif page == "Nifty 50 Stock Scanner":
                    page4.display_page()

        elif st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")
            if st.button("Register"):
                st.session_state.register = True
                st.experimental_rerun()

        elif st.session_state["authentication_status"] is None:
            st.warning("Please enter your username and password")
            if st.button("Register"):
                st.session_state.register = True
                st.experimental_rerun()

if __name__ == "__main__":
    main()
