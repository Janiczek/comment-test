import streamlit as st

def main():
    st.set_page_config(layout="wide")
    st.title("Foo")
    if st.button("Bar", key="btn"):
        with st.container(key="ack"):
            st.write("Bar'd successfully!")

if __name__ == "__main__":
    main()