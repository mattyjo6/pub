import pandas as pd
import streamlit as st
import plotly.express as px

# Load the London Pubs dataset
def load_data():
    return pd.read_excel("open_pubs_10000_sample.xlsx")

# Function to filter pubs by local authority and display on map
def display_pubs_by_authority(authority_name, df):
    authority_pubs = df[df['local_authority'] == authority_name]

    # Check if 'name' column exists in the dataset
    if 'name' in authority_pubs.columns:
        # Create an interactive map using Plotly
        fig = px.scatter_mapbox(authority_pubs, lat="latitude", lon="longitude", hover_name="name",
                                zoom=10, height=500)
        fig.update_layout(mapbox_style="open-street-map")

        # Display the map
        st.plotly_chart(fig)
    else:
        st.error("Dataset does not contain a 'name' column.")

# Main Streamlit app
def main():
    st.title("London Pubs Explorer")

    # Load the data
    df = load_data()

    # Sidebar input for local authority
    authority_name = st.sidebar.text_input("Enter Local Authority", "Westminster")

    # Show button only if user has entered an authority name
    if authority_name:
        if st.sidebar.button("Show Pubs"):
            display_pubs_by_authority(authority_name, df)

if __name__ == "__main__":
    main()


