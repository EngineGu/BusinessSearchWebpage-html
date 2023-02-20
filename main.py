from flask import Flask, render_template,request,jsonify
import requests

MY_YELP_API_KEY = ""

def call_get_businesses_api(keyword,latitude,longitude,distance,category):
    # set url
    search_api_url = 'https://api.yelp.com/v3/businesses/search'
    # set authorization
    headers = {'Authorization': 'Bearer {}'.format(MY_YELP_API_KEY)}
    # set params
    if (distance < 512):
        radius = int(distance * 1609.34) # miles to meters
        params = {
            "term": keyword, 
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
            "categories": category
            }
    else:
        params = {
            "term": keyword, 
            "latitude": latitude,
            "longitude": longitude,
            "categories": category
            }

    # send request and get response 
    response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
    return response.json()

def call_get_business_detail_api(business_id):
    # set url
    search_api_url = 'https://api.yelp.com/v3/businesses/{id}'.format(id=business_id)
    # set authorization
    headers = {'Authorization': 'Bearer {api_key}'.format(api_key=MY_YELP_API_KEY)}
    # send request and get response 
    response = requests.get(search_api_url, headers=headers, timeout=5)
    return response.json()

app = Flask(__name__)

@app.route('/homePage')
def homePage():
    return app.send_static_file('./static/html/business.html')

@app.route("/businesses/search",methods=["GET"])
def search_businesses():
    keyword = str(request.args.get("keyword"))
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    distance = float(request.args.get("distance"))
    category = str(request.args.get("category"))
    response = jsonify(call_get_businesses_api(keyword,latitude,longitude,distance,category))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/businesses/<string:business_id>",methods=["GET"])
def get_business_detail(business_id):
    response = jsonify(call_get_business_detail_api(business_id))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)