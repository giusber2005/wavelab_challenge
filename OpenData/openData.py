import requests
import os
from datetime import datetime,timezone
import math

def main():

    # Get the current date
    current_date = datetime.now()
    date = current_date.strftime('%Y-%m-%d')
    season = get_season(current_date)

    # get location of the EV station
    location = [46.47858328296116,11.332559910750518]

    # get time remaing for full charge
    time_avilable = 3

    # seach new data 
    good_quality_data = {'Time':time_avilable}

    for activity_type in [1,season,8,32,64,128]:
        call_activity = f'https://tourism.api.opendatahub.com/v1/ODHActivityPoi?pagenumber=1&type={activity_type}&active=true&latitude={location[0]}&longitude={location[1]}&radius=3000&removenullvalues=false'
        Activity = requests.get(call_activity)
        Activity = Activity.json()
        good_quality_data = create_text_acttivity(Activity,location,good_quality_data)

    call_event = f'https://tourism.api.opendatahub.com/v1/Event?pagenumber=1&active=true&begindate={date}&enddate={date}&latitude={location[0]}&longitude={location[1]}&radius=3000&removenullvalues=false'
    Event = requests.get(call_event)
    Event = Event.json()
    good_quality_data = create_text_event(Event,location,good_quality_data)
    
    call_meteo = f'https://tourism.api.opendatahub.com/v1/Weather/Forecast?language=en&latitude={location[0]}&longitude={location[1]}&radius=3000'
    Meteo = requests.get(call_meteo)
    Meteo = Meteo.json()
    # Extract the next two entries with dates after the current date
    filtered_data = [entry for entry in Meteo[0]['Forecast3HoursInterval'] if datetime.strptime(entry['Date'], '%Y-%m-%dT%H:%M:%S%z') > datetime.now(timezone.utc)]
    # Limit to the next two entries
    good_quality_data['wheather forcast'] = {'desc': 'weather forcast of the next 3 hours','contact':filtered_data[1]}


        
    
    text = generate_text(good_quality_data)

    # create output folder
    if not os.path.exists('OpenData/data_input'):
        os.makedirs('OpenData/data_input')

    with open('OpenData/data_input/activity.txt', 'w') as file:
        file.write(text)

    

    # create output folder
    if not os.path.exists('OpenData/data_input'):
        os.makedirs('OpenData/data_input')

    with open('OpenData/data_input/activity.txt', 'w') as file:
        file.write(text)

    
def get_season(date):
    # Define the start dates of the seasons
    spring = datetime(date.year, 3, 20)
    summer = datetime(date.year, 6, 21)
    fall = datetime(date.year, 9, 22)
    winter = datetime(date.year, 12, 21)
    
    # Compare the current date to the start dates of the seasons
    if spring <= date < summer:
        return 4
    elif summer <= date < fall:
        return 4
    elif fall <= date < winter:
        return 2
    else:
        return 2

def create_text_acttivity(activity,location,good_quality_data:dict):
    if len(activity['Items'])>0:
        for id in range(len(activity['Items'])):
            name = activity['Items'][id]['Detail']['en']['Title']
            location_act = activity['Items'][id]['GpsInfo'][0]
            dist = haversine(location[0], location[1], location_act['Latitude'], location_act['Longitude'])
            contact = {}
            for n,content in activity['Items'][id]['ContactInfos']['en'].items():
                if content!=None:
                    contact[n] = content
            good_quality_data[str(name)] = {'desc':activity['Items'][id]['Detail']['en']['MetaDesc'],
                                                                                    'contact': contact,
                                                                                    'dist':dist}
            

    return good_quality_data

def create_text_event(event,location,good_quality_data):
    if len(event['Items'])>0:
        for id in range(len(event['Items'])):
            name = event['Items'][id]['Detail']['en']['BaseText']
            location_act = event['Items'][id]['GpsInfo'][0]
            dist = haversine(location[0], location[1], location_act['Latitude'], location_act['Longitude'])
            contact = {}
            for n,content in event['Items'][id]['ContactInfos']['en'].items():
                if content!=None:
                    contact[n] = content
            good_quality_data[str(name)] = {'desc':event['Items'][id]['Detail']['en']['MetaDesc'],
                                                                                    'contact': contact,
                                                                                    'dist':dist}
    return good_quality_data

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of Earth in meters
    R = 6371000
    
    # Calculate the distance
    distance = R * c
    return round(distance)

# Example usage



def generate_text(data):
    lines = []
    for name, details in data.items():
        
        if name == 'Time':
            lines.append(f"Time availabe before the full charge of the car':{details}\n")
        else:
            lines.append(f"Name: {name}\n")
            lines.append(f"Description: {details['desc']}\n")
            lines.append("Contact Information:\n")
            for key, value in details['contact'].items():
                lines.append(f"  {key}: {value}\n")
            try:
                lines.append(f"Distance in meters from the EV station: {details['dist']}\n")
            except:
                pass
            
        lines.append("\n")
    return ''.join(lines)


if __name__ == "__main__":
    main()
