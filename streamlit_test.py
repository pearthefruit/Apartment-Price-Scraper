import streamlit as st
import pandas as pd
import os
import altair as alt
import platform

# Define file paths for each dataset
haus_filename = 'Haus25_apt_data.csv'
beach_filename = 'theBeach_data.csv'
hendrix_filename = 'Hendrix_data.csv'
dutch_filename = '19Dutch.csv'

if platform.system() == 'Windows':
    filepath = r'C:\Users\peary\OneDrive - The City University of New York\Web Scraping\Rental'
elif platform.system() == 'Darwin':
    filepath = r'/Users/pearsonyam/Library/CloudStorage/OneDrive-TheCityUniversityofNewYork/Web Scraping/Rental'
else:
    raise Exception("unsupported OS")

haus_filepath = os.path.join(filepath, haus_filename)
beach_filepath = os.path.join(filepath, beach_filename)
hendrix_filepath = os.path.join(filepath, hendrix_filename)
dutch_filepath = os.path.join(filepath, dutch_filename)

# Load datasets
haus_df = pd.read_csv(haus_filepath)
haus_df['price'] = haus_df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

beach_df = pd.read_csv(beach_filepath)
beach_df['price'] = beach_df['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

hendrix_df = pd.read_csv(hendrix_filepath)

dutch_df = pd.read_csv(dutch_filepath)
def clean_price(price):
    if isinstance(price, str):
        # Remove 'Starting at $' and commas if present
        price = price.replace('Starting at $', '').replace(',', '').strip()
        # Check if the remaining price is numeric
        if price.replace('.', '', 1).isdigit():
            return float(price)
    return None  # Return None for non-numeric values like 'Call for Pricing'
# Apply the function to the price column
dutch_df['price'] = dutch_df['price'].apply(clean_price)


# Create tabs for each apartment building
tabs = st.tabs(["Haus25", "The Beach", "Hendrix", "19 Dutch"])

# Haus25 Tab
with tabs[0]:
    st.write('# Haus25') # haus section start
    st.bar_chart(data=haus_df, x='scraped_date', y='price', y_label='price')

    # haus bar chart
    haus_chart = alt.Chart(haus_df).mark_bar().encode(
        x='scraped_date',
        y=alt.Y('price:Q', aggregate='count', title='price'),
        color='layout:N',
        tooltip=[alt.Tooltip('title:N', title='Apartment Title'),
        alt.Tooltip('price:Q', title='Price'),
        alt.Tooltip('layout:N', title='Layout'),
        alt.Tooltip('floor_plan', title='Floor Plan'),
        alt.Tooltip('availability', title='Availability')
        ]
    )
    st.write(haus_chart)

    fp_chart = alt.Chart(haus_df).mark_line().encode(
        x='scraped_date',
        y=alt.Y('price'),
        color='floor_plan:N',
        tooltip=[alt.Tooltip('title:N', title='Apartment Title'),
             alt.Tooltip('price:Q', title='Price'),
             alt.Tooltip('layout:N', title='Layout'),
             alt.Tooltip('floor_plan', title='Floor Plan'),
             alt.Tooltip('availability', title='Availability')
             ]
    ).facet(
        facet='layout:N',
        columns=2
    ).interactive()
    st.write(fp_chart)

    # by layout
    haus_chart2 = alt.Chart(haus_df).mark_point(shape='square').encode(
        x=alt.X('scraped_date'),
        # x=alt.X('scraped_date:T', axis=alt.Axis(format='%Y-%m-%d', title='Scraped Date')),
        y=alt.Y('price'),
        color='layout:N',
        tooltip=[alt.Tooltip('title:N', title='Apartment Title'),  # Add title to tooltip
             alt.Tooltip('price:Q', title='Price'),
            #  alt.Tooltip('scraped_date:T', title='Date', format='%Y-%m-%d'), # screws up the x axis date formatting
             alt.Tooltip('layout:N', title='Layout'),
             alt.Tooltip('floor_plan', title='Floor Plan'),
             alt.Tooltip('availability', title='Availability')
             ]
    ).facet(
        facet='layout:N',
        columns=2
    # ).configure_legend(
    #     title=None
    ).interactive()

    st.write(haus_chart2)



    # show haus data table
    st.write(haus_df)

# The Beach Tab
with tabs[1]:
    st.write('# The Beach')
    st.bar_chart(data=beach_df, x='scraped_date', y=['price'], y_label='price')

    # grouped bar
    beach_bar = alt.Chart(beach_df).mark_bar().encode(
        x=alt.X('scraped_date'),
        y=alt.Y('price', aggregate='count'),
        color='layout:N',
        tooltip=[alt.Tooltip('title:N', title='Apartment Title'),
                 alt.Tooltip('price:Q', title='Price'),
                 alt.Tooltip('area', title='sqft'),
                 alt.Tooltip('availability', title='Availability')
                 ]
    )
    st.write(beach_bar)
    st.write(beach_df)

# Hendrix Tab
with tabs[2]:
    st.write('# Hendrix')
    st.bar_chart(data=hendrix_df, x='Date', y='rent', y_label='rent')
    hendrix_chart = alt.Chart(hendrix_df).mark_bar().encode(
        x='Date',
        y=alt.Y('rent', aggregate='count'),
        color='numBedrooms',
        tooltip=[
            alt.Tooltip('name', title='Apartment Title'),
            alt.Tooltip('rent', title='Price'),
            alt.Tooltip('numBedrooms', title='Beds'),
            alt.Tooltip('numBaths', title="Baths"),
            alt.Tooltip('availableStarting', title='Availability')
        ]
    )
    st.write(hendrix_chart)

    hendrix_chart_by_title = alt.Chart(hendrix_df).mark_circle().encode(
        x=alt.X('Date'),
        y=alt.Y('rent'),
        color='numBedrooms',
        tooltip=[
            alt.Tooltip('name', title='Apartment Title'),
            alt.Tooltip('rent', title='Price'),
            alt.Tooltip('numBedrooms', title='Beds'),
            alt.Tooltip('numBaths', title="Baths"),
            alt.Tooltip('availableStarting', title='Availability')
        ]
    ).facet(
        facet='numBedrooms'
    ).interactive()

    st.write(hendrix_chart_by_title)

    st.write(hendrix_df)

# 19 Dutch Tab
with tabs[3]:
    st.write('# 19 Dutch')
    st.bar_chart(data=dutch_df, x='scraped_date', y=['price'], y_label='price')
    dutch_chart = alt.Chart(dutch_df).mark_bar().encode(
        x='scraped_date',
        y=alt.Y('price', aggregate='count'),
        color='bed',
        tooltip=[alt.Tooltip('title:N', title='Apt Title'),
                 alt.Tooltip('price:Q', title='Price'),
                 alt.Tooltip('bed', title='Beds'),
                 alt.Tooltip('bath', title='Baths'),
                 alt.Tooltip('area', title='sqft')
        ]
    )
    st.write(dutch_chart)
    st.write(dutch_df)