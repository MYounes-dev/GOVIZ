import streamlit as st
import pandas as pd
import plotly.express as px

st.write('# Hotel Bookings')

st.write('## Home countries of guests')

df = pd.read_csv('hotel_bookings.csv')

source = df

type_radio = st.radio(
     "Choose a hotel type",
     ('Resort Hotel', 'City Hotel', 'All'))


if type_radio == 'Resort Hotel':
    mask = df.hotel == "Resort Hotel"
    
if type_radio == 'City Hotel':
    mask = df.hotel == "City Hotel"

if type_radio == 'All':
    mask = [True]*len(df)

source = df[mask]

country_data = pd.DataFrame(source.loc[source["is_canceled"] == 0]["country"].value_counts())
country_data.rename(columns={"country": "Number of Guests"}, inplace=True)
total_guests = country_data["Number of Guests"].sum()
country_data["Guests in %"] = round(country_data["Number of Guests"] / total_guests * 100, 2)
country_data["country"] = country_data.index

# show on map
guest_map = px.choropleth(country_data,
                    locations=country_data.index,
                    color=country_data["Guests in %"], 
                    hover_name=country_data.index, 
                    color_continuous_scale=px.colors.sequential.Electric_r,
                    title="Home country of guests (grey zones have unknown data)")
guest_map.update_layout( autosize=False, width=500, height=500)

st.plotly_chart(guest_map, use_container_width=True)


st.write('## Evolution of the average daily rate')
df.arrival_date_year = df.arrival_date_year.astype('str')

sorted_dates = [
                  ('2015','July'),
                 ('2015','August'),
                 ('2015','September'),
                 ('2015','October'),
                 ('2015','November'),
                 ('2015','December'),
                ('2016','January'),
                 ('2016','February'),
                 ('2016','March'),
                 ('2016','April'),
                 ('2016','May'),
                 ('2016','June'),
                 ('2016','July'),
                 ('2016','August'),
                 ('2016','September'),
                 ('2016','October'),
                 ('2016','November'),
                 ('2016','December'),
                ('2017','January'),
                 ('2017','February'),
                 ('2017','March'),
                 ('2017','April'),
                 ('2017','May'),
                 ('2017','June'),
                 ('2017','July'),
                 ('2017','August')
               ]

sorted_dates_transformed = {
                   '2015 July': 'Jul. 2015' ,
                  '2015 August': 'Aug. 2015',
                  '2015 September':'Sep. 2015' ,
                  '2015 October': 'Oct. 2015',
                  '2015 November': 'Nov. 2015', 
                  '2015 December': 'Dec. 2015',
                 '2016 January': 'Jan. 2016',
                  '2016 February': 'Feb. 2016',
                  '2016 March': 'Mar. 2016',
                  '2016 April' :'Apr. 2016',
                  '2016 May' :'May 2016',
                  '2016 June': 'Jun. 2016',
                  '2016 July' :'Jul. 2016',
                  '2016 August':'Aug. 2016' ,
                  '2016 September' :'Sep. 2016',
                  '2016 October' :'Oct. 2016',
                  '2016 November': 'Nov. 2016',
                  '2016 December': 'Dec. 2016',
                 '2017 January':'Jan. 2017' ,
                  '2017 February' :'Feb. 2017',
                  '2017 March' :'Mar. 2017',
                  '2017 April' :'Apr. 2017',
                  '2017 May' :'May 2017',
                  '2017 June': 'Jun. 2017',
                  '2017 July' :'Jul. 2017',
                  '2017 August':'Aug. 2017'                    
}

prices_mean = {}
prices_std = {}

for type_of_hotel in ['Resort Hotel', 'City Hotel']:
   df_mean = df[(df.is_canceled == 0) & (df.hotel == type_of_hotel)].groupby([ 'arrival_date_year', 'arrival_date_month']).mean()['adr'].loc[sorted_dates].copy()
   df_mean.index = df_mean.index.map(' '.join)

   df_std = df[(df.is_canceled == 0) & (df.hotel == type_of_hotel)].groupby([ 'arrival_date_year', 'arrival_date_month']).std()['adr'].loc[sorted_dates].copy()
   df_std.index = df_std.index.map(' '.join)

   prices_mean[type_of_hotel] = df_mean
   prices_std[type_of_hotel] = df_std
   
d1 = pd.DataFrame(prices_mean['City Hotel'])
d1['hotel'] = 'City Hotel'
d1.reset_index(inplace = True)
d1.rename(columns = {"index" : 'date'}, inplace = True)

d2 = pd.DataFrame(prices_mean['Resort Hotel'])
d2['hotel'] = 'Resort Hotel'
d2.reset_index(inplace = True)
d2.rename(columns = {"index" : 'date'}, inplace = True)

d = pd.concat([d1,d2], axis = 0)

if type_radio == 'Resort Hotel':
    mask = d.hotel == "Resort Hotel"
    
if type_radio == 'City Hotel':
    mask = d.hotel == "City Hotel"

if type_radio == 'All':
    mask = [True]*len(d)

d = d[mask]

fig = px.line(d, x="date", y="adr", color = 'hotel')
st.plotly_chart(fig)


st.write("## Number of guests in Resort / City Hotels")

from datetime import datetime
slider_value = st.slider(
     "Choose a date",
     min_value =datetime(2015, 7, 1),
     max_value = datetime(2017, 8, 1),
     value=datetime(2016, 1, 1),
     format="MM/YYYY")

df["Date"] = df['arrival_date_year'] + ' ' + df['arrival_date_month']
df["Date"] = pd.to_datetime(df['Date'])

df = df[df.Date <= slider_value]

m1 = (df['hotel'] == 'Resort Hotel').mean()
m2 = 1-m1
d = pd.DataFrame.from_dict({"Resort Hotel" : [m1], "City Hotel" : [m2]})
st.bar_chart(d, use_container_width  = False, width = 200)
