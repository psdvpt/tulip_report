import streamlit as st
import pandas as pd
import math
from pathlib import Path
import glob

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

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

gdp_df = get_gdp_data()
df = pd.read_parquet('junk.parquet')
print(df)
# Using object notation
selected_id = st.sidebar.selectbox(
    "Select Site",
    df['site_name']
)
selected_row = df[df['site_name'] == selected_id]
print('Selected row = ', selected_row)
site_names = selected_row["site_name"].to_list()
print('site_name',site_names[0])

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: TULP Report

View the M2C data for a selection of sites in Canada.
'''

# Add some spacing
''
''

st.write(df)

pattern = '/home/andy/Downloads/rf_data_imaging/*_*_{}_*.jpg'.format(site_names[0])
file_paths = glob.glob(pattern)

if file_paths:
    print(file_paths)  # prints the first matching file path
else:
    print("No files found matching the pattern")

st.write(selected_row)

st.image('1_2_A1094_1.jpg')

for str_img in file_paths:
    st.image(str_img, caption="M2c data for ...")


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: TULP Report

View the M2C data for a selection of sites in Canada.
'''

# Add some spacing
''
''

