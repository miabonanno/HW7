import aiml
import os
import requests
import json



#darksky_API_key= '4a0994234cd2b79d85e8f1d5cdc72236'

# kernel is responsible for responding to users
kernel = aiml.Kernel()

# load every aiml file in the 'standard' directory
# use os.listdir and a for loop to do this
for x in os.listdir('aiml_data'):
	kernel.learn(os.path.join('aiml_data', x))
	#kernel.learn(os.path.join('aiml_data', 'std-hello.aiml'))


# add a new response for when the user says "example * and *"
# note that the ARGUMENT NAMES (first and second) must match up with
# the names in kernel.addPattern


CACHE_FNAME = 'cache.json'

try:
	cahce_file = open(CACHE_FNAME, 'r')
	cahce_contents = cahce_file.read()
	cahce_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def getWithCaching(baseURL, params = {}):
	req = requests.Request(method = 'GET',  url = baseURL, params = sorted(params.items()))
	prepped = req.prepare()
	fullURL = prepped.url

	if fullURL not in CACHE_DICTION:

		response = requests.Session().send(prepped)
		CACHE_DICTION[fullURL] = response.text

		cache_file = open(CACHE_FNAME, 'w')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return CACHE_DICTION[fullURL]

#def exampleResponse(first, second):
    #return 'first arg is {}, second arg is {}'.format(first, second)
#kernel.addPattern("example {first} and {second}", exampleResponse)

def getWeather(city):
	geo_url = "https://maps.googleapis.com/maps/api/geocode/json?"
	geocoding_API_key = 'AIzaSyDUIPpWscDIuAYAyKdEU6lQTP01QhC4ez4'
	geo_params = {'address': city, 'key': geocoding_API_key}
	geo_request = getWithCaching(geo_url, params = geo_params)
	geo_data = json.loads(geo_request)
	try:
		latitude = geo_data['results'][0]['geometry']['location']['lat']
		longitude = geo_data['results'][0]['geometry']['location']['lng']
	except:
		return 'Is {} a city?'.format(city)

	DS_URL = "https://api.darksky.net/forecast/26de71ce03315ba2aaef226b5b655892/{},{}".format(latitude,longitude)

	DS_request = getWithCaching(DS_URL)

	try:
			answer = json.loads(DS_request)
	except:
			answer = "Sorry, I don't know."
	return answer


def WeatherLike(city):
	city_name= getWeather(city)
	weather_status = city_name['currently']['summary']
	return "The weather in {} is {}.".format(city, weather_status)


def RainyDayProbability(city):
	rain_data = getWeather(city)
	rain_probability = rain_data['daily']['data'][0]['precipProbability']
	if rain_probability < 0.1:
		return "It almost definitely will not rain in {} today.".format(city)
	elif rain_probability >= 0.1 and rain_probability < 0.5:
		return "It probably will not rain in {} today.".format(city)
	elif rain_probability >= 0.5 and rain_probability <0.9:
		return "It probably will rain in {} today.".format(city)
	elif rain_probability >= 0.9:
		return "It will almost definitely rain in {} today.".format(city)


def howHot(city):
	today_temp = getWeather(city)
	HottestTemp = today_temp['daily']['data'][0]['temperatureMax']
	return ('In {} it will reach {} today.'.format(city, HottestTemp))


def howCold(city):
	today_temp = getWeather(city)
	ColdestTemp = today_temp['daily']['data'][0]['temperatureMin']
	return "In {} it will get to {}.".format(city, ColdestTemp)


def RainyWeekProbability(city):
	rainyweek_data = getWeather(city)
	if type(rainyweek_data) == type(""):
		return rainyweek_data

	rain_likelihood=[(1-x['precipProbability']) for x in rainyweek_data['daily']['data']]
	total = 1
	for x in rain_likelihood[0:7]:
		total *= x
	rain_probability= 1-total
	if rain_probability < 0.1:
		return "It almost definitely will not rain in {} this week.".format(city)
	elif rain_probability >= 0.1 and rain_probability < 0.5:
		return "It probably will not rain in {} this week.".format(city)
	elif rain_probability >= 0.5 and rain_probability <0.9:
		return "It probably will rain in {} this week.".format(city)
	elif rain_probability >= 0.9:
		return "It will almost definitely rain in {} this week.".format(city)


def howHotWeek(city):
	week_data = getWeather(city)
	if type (week_data)== type(""):
		return week_data

	daily_high= [day['apparentTemperatureMax'] for day in week_data['daily']['data']]
	return 'In {} it will reach {} this week.'.format(city, max(daily_high))


def howColdWeek(city):
	week_data2= getWeather(city)
	if type(week_data2) == type (""):
		return week_data2

	daily_low = [day['apparentTemperatureMin'] for day in week_data2['daily']['data']]
	return 'In {} it will drop to {} this week.'.format(city, min(daily_low))



kernel.addPattern("What's the weather like in {city}?", WeatherLike)
kernel.addPattern("Is it going to rain in {city} today?", RainyDayProbability)
kernel.addPattern("How hot will it get in {city} today?", howHot)
kernel.addPattern("How cold will it get in {city} today?", howCold)
kernel.addPattern("Is it going to rain in {city} this week?", RainyWeekProbability)
kernel.addPattern("How hot will it get in {city} this week?", howHotWeek)
kernel.addPattern("How cold will it get in {city} this week?", howColdWeek)



user_input = ''
while user_input != 'exit':
	user_input = raw_input('> ')
	print '...{}\n'.format(kernel.respond(user_input))
