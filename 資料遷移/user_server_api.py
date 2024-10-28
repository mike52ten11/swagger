import sqlite3
import requests
from datetime import datetime
import time
from zoneinfo import ZoneInfo



# 配置
LOCAL_DB_PATH = r'db.sqlite3'
ENDPOINT = 'http://10.52.15.201:80'
TOKEN = 'ee10d9bdfa9eff10eb9321a71a7cebeeb65f2fd4'
Admin_TOKEN = '43087078d191b314f9350084b27e7f7b6071fe18'

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

        def disable(self, data):    
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}       
            data['registered'] = 0 
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False 

        def enable(self, data):    
            API_ENDPOINT = f'{ENDPOINT}/ami-api/device-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}     
            data['registered'] = 1
            
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False 

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

        def disable(self, data):    
            API_ENDPOINT = f'{ENDPOINT}/ami-api/electricnumber-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}     
            data['registered'] = 0  
            
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False 

        def enable(self, data):   
            API_ENDPOINT = f'{ENDPOINT}/ami-api/electricnumber-register/'
            headers = {'Authorization': f'Token {Admin_TOKEN}'}     
            data['registered'] = 1
            
            try:
                response = requests.patch(API_ENDPOINT, json=data, headers=headers)
                response.raise_for_status()
                print(f"Data sent successfully: {response.json()}")
                return True

            except requests.exceptions.RequestException as e:
                print(f"Error sending data: {response.json()}")
                return False 


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

    def banding(self, data):
        API_ENDPOINT = f'{ENDPOINT}/ami-api/user-binding/'
        headers = {
            'Authorization': f'Token {TOKEN}',
            'Content-Type': 'application/json'
        }        
        
        try:
            response = requests.post(API_ENDPOINT, json=data, headers=headers)
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


if __name__ == "__main__":

    '''
    註冊使用者帳號
    '''
    # data = {
    #     'username':'0900123456',
    #     'password':'012345678'

    # }
    # user1 = Customer()
    # user1.register(data)


    # data = {
    #     'electricnumber':'01234567890'
    # }
    # user1 = Customer()
    # user1.banding(data)    

    '''
    註冊/啟用/停用/電號
    '''
    # data = {
        
    #     'electricnumber':'01234567890',

    # }
    # admin = Admin().ElectricNumber()
    # admin.register(data)  #註冊 
    # admin.disable(data)  #停用

    '''
    註冊裝置
    '''
    # data = {
    #     "deviceuuid": '8dc09891-2d5f-46fc-9947-043ba422c452',
    #     "name": "設備1"
    # }
    # admin = Admin().Device()
    # # admin.disable(data)
    # admin.register(data)      
    '''
      綁定電號和裝置
    '''
    data = {
        "deviceuuid": '8dc09891-2d5f-46fc-9947-043ba422c452',
        'electricnumber':'01234567890',
    }
    admin = Admin().ElectricNumber_Device_Band()
    admin.band(data)       
    