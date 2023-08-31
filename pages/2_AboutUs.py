import streamlit as st



def about_us():
    st.markdown(
        """
        <style>
        .stApp {
            background: url(https://img.freepik.com/free-photo/vintage-pink-telephone-composition_23-2148913955.jpg?w=996&t=st=1693475056~exp=1693475656~hmac=6188d939872f5304547982a8e566b0feca7ffa57f45b82144bd7ef9c7e3ef0d1) no-repeat center center;
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("About Us")

    st.write("""
    Welcome to our application! We are a diverse group of individuals brought together by our passion for creating impactful and innovative solutions through technology. We are committed to delivering excellence and enhancing user experiences.

    If you have any questions, suggestions, or feedback, please don't hesitate to get in touch with us.
    """)

    st.header("Our Aim")

    st.write("""
    The aim of our project is To develop a machine learning model that can predict the future prices of various cryptocurrencies based on the past data.""")

    st.header("Meet the Team")
    col1,col2,col3=st.columns(3)

    with col1:
        st.subheader("Arpit Tiwari")
        btn_col1,btn_col2,btn_col3 = st.columns(3)
        with btn_col1:
            link_icon = '<a href="https://www.linkedin.com/in/arpit-tiwari-a82410185/" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col2:
            link_icon = '<a href="https://github.com/arpit512" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col3:
            link_icon = '<a href="mailto:tiwariarpit512@gmail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        st.subheader("Deepak Patel")
        btn_col4, btn_col5, btn_col6 = st.columns(3)

        with btn_col4:
            link_icon = '<a href="https://www.linkedin.com/in/deepakpatel001/" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col5:
            link_icon = '<a href="https://github.com/Deepakpatel001" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'

            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col6:
            link_icon = '<a href="mailto:deepakpatel970@gmail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)

    with col2:
        st.subheader("Charudatta Patil")
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            link_icon = '<a href="http://linkedin.com/in/charudatta-patil-9782a01b5" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col2:

            link_icon = '<a href="https://github.com/charudatta-17/Crypto_Currency_price_prediction.git" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col3:

            link_icon = '<a href="mailto:charudatta292@gmail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)

        st.subheader("Aditya Ugale")
        btn_col4, btn_col5, btn_col6 = st.columns(3)
        with btn_col4:
            link_icon = '<a href="https://www.linkedin.com/in/aditya-ugale-45563a200" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col5:
            link_icon = '<a href="https://github.com/aditya4566" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col6:
            link_icon = '<a href="adityaugale79@mail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
    with col3:

        st.subheader("Aishwarya")
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            link_icon = '<a href="https://www.linkedin.com/in/aishwarya-chopade" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col2:
            link_icon = '<a href="https://github.com/aishwarya199808" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col3:
            link_icon = '<a href="mailto:ashchopade.mum.dbda@gmail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)

        st.subheader("Ushashree")
        btn_col4, btn_col5, btn_col6 = st.columns(3)
        with btn_col4:
            link_icon = '<a href="https://www.linkedin.com/in/ushashreeshripati/" target="_blank"><img src="https://img.icons8.com/?size=1x&id=xuvGCOXi8Wyg&format=png" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col5:
            link_icon = '<a href="https://github.com/Ushashree441997" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)
        with btn_col6:
            link_icon = '<a href="mailto:ushashripati41997@gmail.com"><img src="https://www.logo.wine/a/logo/Gmail/Gmail-Logo.wine.svg" width="40" height="20"></a>'
            st.markdown(link_icon, unsafe_allow_html=True)


    st.write("""
    Our team brings together a wide range of skills and expertise, from software development and design to data science and content creation. This diversity enables us to tackle complex challenges and deliver innovative solutions.
    """)

    st.subheader("Contact Us")

    st.write("""
    If you have any questions or would like to connect with us, feel free to send an email to [techcollective.in](mailto:techcollective.in)
    """)


# Main app
def main():
    st.set_page_config(page_title="About Us", page_icon=":information_source:")
    about_us()


if __name__ == "__main__":
    main()


