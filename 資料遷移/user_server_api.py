import sqlite3
import requests
from datetime import datetime
import time
from zoneinfo import ZoneInfo



# 配置
LOCAL_DB_PATH = r'db.sqlite3'
ENDPOINT = 'http://10.52.15.201:80'
TOKEN = '284c9497643c60bffaf0f6880a317fa1a21adfd6'
Admin_TOKEN = '0158f46bd0fb61c03f6ffff33d9f1eb03d28e329'

class Admin:
    class Device:

        def register(self,data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.post(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False  

        def delete(self):
            pass

        def disable(self):    
            pass

        def enable(self):    
            pass

        def rename(self,data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False             


    class User:
        def disable(self):    
            pass

        def enable(self):    
            pass

        def info(self, data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/token/'
            
            
            try:
                response = requests.post(API_ENDPOINT, json=data)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False    

    class ElectricNumber:

        def register(self, data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/electricnumber-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.post(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False

        def delete(self):
            pass

        def disable(self):    
            pass

        def enable(self):    
            pass

        def rename(self,data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/electricnumber-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False 

    class ElectricNumber_Device_Band:

        def band(self, data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-binding/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.post(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False

        def unband(self):
            pass

        def info(self, data):
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-binding/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            
            try:
                response = requests.get(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False

class Customer:

    def register(self, data):
        API_ENDPOINT = f'{ENDPOINT}/ami-api/user-register/'
        
        
        try:
            response = requests.post(API_ENDPOINT, json=data)
            response.raise_for_status()
            print(f"Data sent successfully: {response.json()}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {response.json()}")
            return False


    def info(self, data):
        API_ENDPOINT = f'{ENDPOINT}/ami-api/token/'
        
        
        try:
            response = requests.post(API_ENDPOINT, json=data)
            response.raise_for_status()
            print(f"Data sent successfully: {response.json()}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {response.json()}")
            return False





class ComparisonTable:

    def electricnumber_device(self): #一對一    
        pass

    def user_electricnumber(self):   #一對多 
        pass

class AMIData:

    def send(self):    
        pass

    def get(self):    
        pass


def read_data_from_sqlite():
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT deviceUuid, generatedTime, value FROM writedata_ami")
    rows = cursor.fetchall()
    conn.close()
    return rows

def send_data_to_server(data):
    API_ENDPOINT = f'{ENDPOINT}/api/devicedata/'
    TOKEN = "52542783702f7051ae2663133e084b67f1b9eea8"
    # TOKEN = "7488b1681692f0dfbda173ace66f2a2421673302"
    headers = {'Authorization': f'Token {TOKEN}'}
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    try:
        if response.status_code==400:
            print(f"時間: {datetime.fromtimestamp(data['datatime']/1000,ZoneInfo('Asia/Taipei'))}")
            print("重複上傳")
            return False 
        response.raise_for_status()
        # print(f"Data sent successfully: {response.json()}")
        print(f"時間: {datetime.fromtimestamp(data['datatime']/1000,ZoneInfo('Asia/Taipei'))}")
        print(f"Data sent successfully: {data['deviceuuid']}")
        return True
    except requests.exceptions.RequestException as e:
        
        print(f"時間: {datetime.fromtimestamp(data['datatime']/1000,ZoneInfo('Asia/Taipei'))}")
                
        print(f"Error sending data: {e}")
        return False

def main():
    rows = read_data_from_sqlite()
    for row in rows:
        deviceuuid, generatedTime, value = row
        data = {
            "deviceuuid": deviceuuid,
            "name": "name1",  # 假設所有設備都是 'name1'，根據需要調整
            "value": value,
            "datatime": generatedTime,
            "createtime": int(time.time())
        }
        success = send_data_to_server(data)
        if not success:
            print(f"Failed to send data for device: {deviceuuid}")
        # time.sleep(1)  # 增加延遲以避免過快發送請求

def get_ami_data():
    API_ENDPOINT = f'{ENDPOINT}/api/getamidata/'
    
    data = {
        "electricnumber": "01234567890",
        "account":"0900123456",
        "start": "1701561600000",
    }    
    TOKEN = "6875193b5449f4e12b0ff81ec632a77cefe1fd2d"
    # TOKEN = "7488b1681692f0dfbda173ace66f2a2421673302"
    headers = {'Authorization': f'Token {TOKEN}'}
    
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(f"Data sent successfully: {response.json()}")
        
        # print(f"Data sent successfully: {data['deviceuuid']}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {response.json()}")
        return False

def register_electricnumber_to_device():
    API_ENDPOINT = f'{ENDPOINT}/api/register_electricnumber_to_device/'
    data = {
        'electricnumber': '01234567890',
        'deviceuuid':  '8dc09891-2d5f-46fc-9947-043ba422c452',
        'registered': 1,
        'account':'0900123456',
        'createtime': "2024-10-23",
    }
    TOKEN = "6875193b5449f4e12b0ff81ec632a77cefe1fd2d"
    headers = {'Authorization': f'Token {TOKEN}'}
    
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(f"Data sent successfully: {response.json()}")

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {response.json()}")
        return False

def get_user_data():
    API_ENDPOINT = f'{ENDPOINT}/api/userinfo/'
    data = {
        "account": "0900123456",
    }
    TOKEN = "6875193b5449f4e12b0ff81ec632a77cefe1fd2d"
    headers = {'Authorization': f'Token {TOKEN}'}
    
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(f"Data sent successfully: {response.json()}")

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {response.json()}")
        return False

def get_user_token():
    API_ENDPOINT = f'{ENDPOINT}/api/api-token-auth/'
    data = {
        "username": "0900123456",
    }
    TOKEN = "52542783702f7051ae2663133e084b67f1b9eea8"
    headers = {'Authorization': f'Token {TOKEN}'}
    
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        print(f"Data sent successfully: {response.json()}")

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")
        return False

if __name__ == "__main__":

    # data = {
    #     "deviceuuid": '8dc09891-2d5f-46fc-9947-043ba422c452',
    #     "name": "name1",  # 假設所有設備都是 'name1'，根據需要調整
    #     "createtime": '2023-10-23'
    # }
    # data = {
    #     'username':'0900123456',
    #     'password':'012345678'

    # }
    # user1 = User()
    # user1.register(data)


    # data = {
    #     'username':'0900123456',
    #     'password':'012345678'

    # }
    # user1 = Customer()
    # user1.info(data)    


    data = {
        'electricnumber':'12345678910',
        'deviceuuid':'8dc09891-2d5f-46fc-9947-043ba422c452'
    }
    admin = Admin().ElectricNumber_Device_Band()
    # admin.rename(data)   
    admin.band(data)  