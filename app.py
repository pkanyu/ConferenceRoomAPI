from flask import *
import pymysql

app = Flask(__name__)
#  First EndPoint -> /register
@app.route('/register', methods =['POST'])
def register():

    # request data from json
    payload = request.json
    username = payload['username']
    phone = payload['phone']
    email = payload['email']
    password = payload['password']
    dob = payload['dob']

    #database connection

    connection = pymysql.connect(host='petersonapi.mysql.pythonanywhere-services.com',user='petersonapi',password='Mmodcom#2023',database='petersonapi$default')
    #cursor
    cursor = connection.cursor()

    # sql
    sql = "insert into users( username, phone, email, password, dob) values(%s,%s,%s,%s,%s)"
    # data
    data = (username,phone,email,password,dob)
    # execute sql, data on a try - except block
    try:
        cursor.execute(sql,data)
        connection.commit()
        response = jsonify({"message": "User Registered Successfully"})
        response.status_code = 201


        return response
    except:
        connection.rollback()
        response = jsonify({"message":"Internal Server Error"})
        response.status_code = 500
        return response
    

@app.route('/login', methods = ['GET'])
def login():
    # get username and password from json payload
    payload = request.json
    username = payload['username']
    password = payload['password']

    # db connection 
    connection = pymysql.connect(host='petersonapi.mysql.pythonanywhere-services.com',user='petersonapi',password='Mmodcom#2023',database='petersonapi$default')

    cursor = connection.cursor()
    # sql
    sql = "select * from users where username = %s and password = %s"

    # data
    data = (username,password)

    # execute sql, data on try except block
    try:
        cursor.execute(sql,data) 
        count = cursor.rowcount
        if count == 0:
            response = jsonify({"message": "Invalid Credential"})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message':'Success'})
            response.status_code = 200
            return response
        
    except:
        response = jsonify({"message":"Internal Server Error"})
        response.status_code = 500
        return response


@app.route("/save_room",methods =["POST"])
def save_room():
    #payload
    payload= request.json
    room_name = payload["room_name"]
    room_cost= payload["room_cost"]
    room_desc = payload["room_desc"]
    availability = payload["availability"]
    image_url = payload["image_url"]

    # connection
    connection = pymysql.connect(host='petersonapi.mysql.pythonanywhere-services.com',user='petersonapi',password='Mmodcom#2023',database='petersonapi$default')
    #cursor
    cursor = connection.cursor()
    #data
    data = (room_name,room_cost,room_desc,availability,image_url) 
    #sql
    sql = " insert into rooms(room_name,room_cost,room_desc,availability,image_url) values(%s,%s,%s,%s,%s)"
    #execute sql, data 
    try:
        cursor.execute(sql,data)
        connection.commit()
        response = jsonify({"message":"Saved Successfully"})
        response.status_code = 201
        return response
    except:
        response =jsonify({"message":"Internal Server Error"})
        response.status_code = 500
        return response


@app.route('/get_rooms',methods=['GET'])
def get_rooms():
    #connection
    connection = pymysql.connect(host='petersonapi.mysql.pythonanywhere-services.com',user='petersonapi',password='Mmodcom#2023',database='petersonapi$default')
    #cursor
    cursor = connection.cursor()
    #sql
    sql = "select * from rooms"
    # Execute cursor
    cursor.execute(sql)
    rooms = cursor.fetchall()
    response =jsonify(rooms)
    response.status_code=200
    return response

from requests.auth import HTTPBasicAuth
import base64
import datetime
import requests
@app.route('/mpesa', methods=['POST'])
def mpesa_payment():
        payload = request.json
        phone = payload['phone']
        amount = payload['amount']

        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(
            consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,

            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Modcom",
            "TransactionDesc": "Modcom"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        
        return jsonify({'message':"Please Check Your Phone to Complete Payment"})








# Connection Setup
# db password: Mmodcom#2023
# host : petersonapi.mysql.pythonanywhere-services.com
# user : petersonapi
# database : petersonapi$default