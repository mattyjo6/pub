import pandas as pd
import streamlit as st
import plotly.express as px

# Load the London Pubs dataset
@st.cache
def load_data():
    return pd.read_excel("open_pubs_10000_sample.xlsx")

df = load_data()

# Function to filter pubs by local authority and display on map
def display_pubs_by_authority(authority_name):
    authority_pubs = df[df['local_authority'] == authority_name]

    # Create an interactive map using Plotly
    fig = px.scatter_mapbox(authority_pubs, lat="latitude", lon="longitude", hover_name="name",
                            zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")

    # Display the map
    st.plotly_chart(fig)

# Function to display a specific pub on the map
def display_specific_pub(pub_name):
    pub_info = df[df['name'].str.contains(pub_name, case=False)]
    if not pub_info.empty:
        fig = px.scatter_mapbox(pub_info, lat="latitude", lon="longitude", hover_name="name", zoom=10, height=500)
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
    else:
        st.error("Sorry, no pub found with that name.")

# Main Streamlit app
def main():
    st.title("London Pubs Explorer")

    # Sidebar input for local authority
    authority_name = st.sidebar.text_input("Enter Local Authority", "Westminster")

    if st.sidebar.button("Show Pubs"):
        display_pubs_by_authority(authority_name)

    st.subheader("Find a Specific Pub")
    pub_name = st.text_input("Enter the name of the pub:")
    if st.button("Show Pub on Map"):
        display_specific_pub(pub_name)

if __name__ == "__main__":
    main()


