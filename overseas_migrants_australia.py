#Topic: Overseas migrants in Australia arrivals and depatures from 2016 to 2023

#---Import the libraries---
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


#---Read the data---

st.set_page_config(page_title="Overseas Arrivals and Departures Australia",
                   page_icon=":bookmark_tabs:",
                   layout="wide")

df = pd.read_excel(
    io='Overseas_Arrivals_and_Departures_Australia.xlsx',
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=3,
    usecols='A:F',
    nrows=1000,)

#---Data Cleaning - Drop rows with missing values---
df.dropna(inplace=True)

# Display the markdown

st.title(":globe_with_meridians: Overseas migrant in Australia arrivals and departures")

# ---SideBar----
st.sidebar.header("Please Filter Here:")

year = st.sidebar.multiselect(
    "Please select the year:",
    options=df["Year"].unique(),
    default=df["Year"].unique())

state = st.sidebar.multiselect(
    "Please select the State:",
    options=df["State"].unique(),
    default=df["State"].unique())

## Filter the data based on user selection

df_selection = df.query(
    "`Year` == @year & `State` == @state" )
#---Check if the dataframe is empty---
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  

st.markdown("---")

    
#---BAR CHART--- The number of migrants arrivals and departures by year
migrants_arrivals_by_year = df_selection[df_selection['Direction'] == 'Overseas migrant arrivals'].groupby(by=["Year"])[["The number of movements"]].sum().sort_values(by="The number of movements")
migrants_departures_by_year = df_selection[df_selection['Direction'] == 'Overseas migrant departures'].groupby(by=["Year"])[["The number of movements"]].sum().sort_values(by="The number of movements")

## Combine the data
combined_data = pd.concat([migrants_arrivals_by_year, migrants_departures_by_year], axis=1)
combined_data.columns = ['Overseas Migrant Arrivals', 'Overseas Migrant Departures']

## Create the grouped bar chart
fig_combined = go.Figure()

fig_combined.add_trace(go.Bar(
    x=combined_data.index,
    y=combined_data['Overseas Migrant Arrivals'],
    name='Overseas Migrant Arrivals',
    marker_color='#d4afb9',
    text=combined_data['Overseas Migrant Arrivals'],  
    textposition='outside' 
))

fig_combined.add_trace(go.Bar(
    x=combined_data.index,
    y=combined_data['Overseas Migrant Departures'],
    name='Overseas Migrant Departures',
    marker_color='#d1cfe2',
    text=combined_data['Overseas Migrant Departures'],  
    textposition='outside' 
))

fig_combined.update_traces(texttemplate='%{text:.2s}') 

fig_combined.update_layout(
    barmode='group',
    title='<b>Overseas Migrant Arrivals vs Departures from 2016 to 2023</b>',
    xaxis=dict(title='Year'),
    yaxis=dict(title='The number of movements', showgrid=False),
    plot_bgcolor='rgba(0,0,0,0)'
)
## Display the Plotly figure in Streamlit

st.plotly_chart(fig_combined,use_container_width=True)


#---Display the Overseas migrant in Australia arrivals and departures---

## Select box 
option = st.selectbox(
    'Please select the direction:',
    ('---','Overseas Migrant Arrivals', 'Overseas Migrant Departures'))

## Display the selected direction

### Perform analysis based on the selected direction

if option == '---':
    st.write('Please select the direction')
    
elif option == 'Overseas Migrant Arrivals':
    
#Total Migrant Arrivals
    
    migrant_arrivals_by_state = df_selection[df_selection['Direction'] == 'Overseas migrant arrivals'].groupby('State')['The number of movements'].sum()
    total_migrant_arrivals = df_selection[df_selection['Direction'] == 'Overseas migrant arrivals']['The number of movements'].sum()
    state_with_highest_arrivals = migrant_arrivals_by_state.idxmax()

    ## Display the data side by side using Streamlit columns

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("🛬 Total migrant arrivals:")
        st.subheader(total_migrant_arrivals)
    with right_column:
        st.subheader(":round_pushpin: Top State for Migrant Arrivals:")
        st.subheader(state_with_highest_arrivals)

 # The total of Overseas migrant arrivals by State Dataframe 
    arrivals_df = df[df['Direction'] == 'Overseas migrant arrivals']
    total_arrivals_by_state = arrivals_df.groupby(['State', 'Direction'])['The number of movements'].sum().reset_index()
    st.subheader("Total Arrivals by State")
    st.dataframe(total_arrivals_by_state, use_container_width=True)
    
# The Permanent arrivals visa types
    permanent_visas_arrivals_df = df_selection[(df_selection['Visa and citizenship groups'] == "Permanent visas") & (df_selection['Direction'] == 'Overseas migrant arrivals')]

    permanent_visas = permanent_visas_arrivals_df.groupby(["Year", "Visa types"])["The number of movements"].sum().reset_index()

    ## Plotting the line chart for migrant arrivals of each permanent visa type over the years
    permanent_arrivals = px.line(permanent_visas, x="Year", y="The number of movements", color="Visa types",
                                  title="Permanent Visas Arrivals",
                                  labels={'The number of movements': 'The number of movements'},
                                  markers=True)


    ## Displaying the line chart
    permanent_arrivals.update_layout(xaxis_title="Year", yaxis_title="The number of movements")
    st.plotly_chart(permanent_arrivals, use_container_width=True)
#The Temporary arrivals visa types

    temporary_visas_arrivals_df = df_selection[(df_selection['Visa and citizenship groups'] == "Temporary visas") & (df_selection['Direction'] == 'Overseas migrant arrivals')]

    temporary_visas = temporary_visas_arrivals_df.groupby(["Year", "Visa types"])["The number of movements"].sum().reset_index()

    # Plotting the line chart for migrant arrivals of each temporary visa type over the years 
    temporary_arrivals = px.line(temporary_visas, x="Year", y="The number of movements", color="Visa types",
                                  title="Temporary visas Arrivals ",
                                  labels={'The number of movements': 'The number of movements'},
                                  markers=True)


    # Displaying the line chart
    
    temporary_arrivals.update_layout(xaxis_title="Year", yaxis_title="The number of movements")

    st.plotly_chart(temporary_arrivals, use_container_width=True)    

elif option == 'Overseas Migrant Departures':
    
#Total Migrant Departures
    migrant_departures_by_state = df_selection[df_selection['Direction'] == 'Overseas migrant departures'].groupby('State')['The number of movements'].sum()
    total_migrant_departures = df_selection[df_selection['Direction'] == 'Overseas migrant departures']['The number of movements'].sum()
    state_with_highest_departures = migrant_departures_by_state.idxmax()
    
    ## Display the data side by side using Streamlit columns

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader(":airplane_departure: Total migrant departures:")
        st.subheader(total_migrant_departures)
    with right_column:
        st.subheader(":round_pushpin: Top State for Migrant Departures:")
        st.subheader(state_with_highest_departures)

 # The total of Overseas migrant departures by State Dataframe 
    departures_df = df[df['Direction'] == 'Overseas migrant departures']
    
    total_departures_by_state = departures_df.groupby(['State', 'Direction'])['The number of movements'].sum().reset_index()
    
    st.subheader("Total Departures by State")
    
    st.dataframe(total_departures_by_state, use_container_width=True)
    
#The Permanent departures visa types
    
    permanent_visas_departures_df = df_selection[(df_selection['Visa and citizenship groups'] == "Permanent visas") & (df_selection['Direction'] == 'Overseas migrant departures')]
    
    permanent_visas_departures = permanent_visas_departures_df.groupby(["Year", "Visa types"])["The number of movements"].sum().reset_index()

    ### Plotting the line chart for migrant departures of each permanent visa type over the years
    permanent_departures = px.line(permanent_visas_departures, x="Year", y="The number of movements", color="Visa types",
                                    title="Permanent Visas Departures",
                                    labels={'The number of movements': 'The number of movements'},
                                    markers=True)


    # Displaying the line chart
    
    permanent_departures.update_layout(xaxis_title="Year", yaxis_title="The number of movements")

    st.plotly_chart(permanent_departures, use_container_width=True)

    ##The Temporary departures visa types
    temporary_visas_departures_df = df_selection[(df_selection['Visa and citizenship groups'] == "Temporary visas") & (df_selection['Direction'] == 'Overseas migrant departures')]

    temporary_visas_departures = temporary_visas_departures_df.groupby(["Year", "Visa types"])["The number of movements"].sum().reset_index()

    ### Plotting the line chart for migrant departures of each temporary visa type over the years
    
    temporary_departures = px.line(temporary_visas_departures, x="Year", y="The number of movements", color="Visa types",
                                    title="Temporary visas Departures ",
                                    labels={'The number of movements': 'The number of movements'},
                                    markers=True)

    # Displaying the line chart
    
    temporary_departures.update_layout(xaxis_title="Year", yaxis_title="The number of movements")

    st.plotly_chart(temporary_departures, use_container_width=True)

st.markdown("---")

