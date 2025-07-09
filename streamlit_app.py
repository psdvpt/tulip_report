import streamlit as st
import pandas as pd
import math
from pathlib import Path
import glob
import folium
from streamlit_folium import folium_static
import os

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Ambiflo',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_canada_data():
    df = pd.read_parquet('tlup_canada.parquet')
    return df
@st.cache_data

def get_atlup_sum()
    df = pd.read_parquet('atlup_sum.parquet')
    return df

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

#gdp_df = get_gdp_data()
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Scope", "TLUP", "ATLUP Summary", "Strength","Quality"])


#df = pd.read_parquet('tlup_canada.parquet')
df = get_canada_data()
#print(df)
# Using object notation
selected_id = st.sidebar.selectbox(
    "Select Site",
    df['site_name'].unique()
)
selected_row = df[df['site_name'] == selected_id]
#print('Selected row = ', selected_row)
site_names = selected_row["site_name"].to_list()
site_name = site_names[0]

# -----------------------------------------------------------------------------
# Draw the actual page   
st.set_page_config(layout="wide")
with tab1:
    st.image('ambiflo_icon.png', width = 300)
    df_loc = pd.read_parquet('tlup_loc.parquet')
    
    st.title("TLUP reports")
    st.write("Prepared for Redwood Infrastructure LP. July 2025")
    st.header("Site Locations")

    # Create a Folium map
    m = folium.Map(location=[52.1304, -100.3468], zoom_start=3)

    # Add markers with labels to the map
    for index, row in df_loc.iterrows():
        popup = "{}: {}".format(index, row['site_id'])
        folium.Marker([row['lat'], row['lon']], popup=popup).add_to(m)


    # Display the map in Streamlit
    folium_static(m)

    st.write("**Locations**")
    with st.container():
        st.write(f'<div style="max-width: 500px;">{df_loc.to_html()}</div>', unsafe_allow_html=True)

with tab2:
    st.header("TLUP")
    st.write("This is the standard TLUP report. Use the other tabs  for ATLUP summary and analysis of signal strength and quality.")
    st.write("Use the list control on the left side panel to select the site and the results will be shown below. The complete table is presented at the foot of this page.")

    # match images with selection
    pattern = '*_*_{}_*.jpg'.format(site_names[0])
    file_paths = glob.glob(pattern)
    sorted_paths = sorted(file_paths, key=lambda x: x.split("/")[-1].split("_")[3])

    str_header = "**{}**".format(site_name)
    st.write(str_header)

    # Highlight Column 2 with a background color
    df_highlighted = selected_row.style.set_properties(**{'background-color': 'yellow'}, subset=['tlup'])
    st.dataframe(df_highlighted)


    for str_img in sorted_paths:
        filename = os.path.basename(str_img)
        #print(filename)  # Output: 1_3_A1094_3.jpg
        parts = filename.split('_')
        last_part = parts[-1].split('.')[0]
        str_range = "Range: {} km".format(last_part)
        st.header(str_range)
        st.image(str_img, caption="M2c data for ...")


    st.header('All Sites')
    # Highlight Column 2 with a background color
    df_highlighted = df.style.set_properties(**{'background-color': 'yellow'}, subset=['tlup'])

    st.dataframe(df_highlighted)


with tab3:
    st.header("ATLUP Summary")
    st.write("**{}**".format(site_name))

    #df_sum = pd.read_parquet('atlup_sum.parquet')
    df_sum = get_atlup_sum()
    selected_row_sum = df_sum[df_sum['site'] == selected_id]

    st.write(selected_row_sum)
    st.write("**All sites**")
    st.write(df_sum)


with tab4:
    st.header("Signal Strength")
    st.write("Analysis of signal strength (rsrp).")

    df_str = pd.read_parquet('atlup_strength.parquet')
    selected_row_str = df_str[df_str['Site'] == selected_id]
    st.write("**{}**".format(selected_id) )  
    st.write(selected_row_str)

    st.write('**All data**')    
    st.write(df_str)

with tab5:
    st.header("Signal Quality")
    st.write("Analysis of signal strength (rsrq).")

    df_qlt = pd.read_parquet('atlup_quality.parquet')
    selected_row_qlt = df_qlt[df_qlt['Site'] == selected_id]
    st.write("**{}**".format(selected_id) )   
    st.write(selected_row_qlt)
    st.write('**All data**')
    st.write(df_qlt)



