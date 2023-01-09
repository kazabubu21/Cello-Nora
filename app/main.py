import os
import sys
from threading import Thread

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import StringProperty

from kivy.core.window import Window

import time
import requests
from kivy.storage.jsonstore import JsonStore


def get_config_path():
    if hasattr(sys, "_MEIPASS"):
        abs_home = os.path.abspath(os.path.expanduser("~"))
        abs_dir_app = os.path.join(abs_home, f".cello_folder")
        if not os.path.exists(abs_dir_app):
            os.mkdir(abs_dir_app)
        cfg_path = os.path.join(abs_dir_app, "data.json")
    else:
        cfg_path = os.path.abspath(".%sdata.json" % os.sep)
    return cfg_path


store = JsonStore(get_config_path())

stop_threads = False

class cell_api():
    def __init__(self, **kwargs):
        self.headers = {
            'Host': 'app.cellopark-il.com',
            'Content-Type': 'application/json',
            'App-Version': '7.70',
            'Device-Os': 'android',
            'Device-Name': 'LGELG-H815',
            'Accept-Language': 'he-IL',
            'App-Key': 'aY5QeL9aaYrmqfoNTjpuW8JTFZy2Ami5+OaP/HsIdXc=',
            'Os-Version': '23',
            'User-Agent': 'Device-LGELG-H815,OS-android,App_version-7.70-null',
            # 'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
        }
        # get a value using a index key and key
        self.auth_token = ""
        self.session_id = ""
        if store.exists('auth_token'):
            self.auth_token =store.get('auth_token')['token']
            if self.auth_token:
                print(self.auth_token)

    def send_sms(self, phone):
        try:
            params = {'userName': phone}
            response = requests.get(
                'https://app.cellopark-il.com/SmartPhoneAPI/Account/VerifyPhone',
                params=params,
                headers=self.headers,
            )
        except:
            pass

    def verifiy_sms(self, phone,sms):
        try:
            json_data = {
                'Password': '',
                'SecretCode': sms,
                'UserName': phone,
            }

            response = requests.post('https://app.cellopark-il.com/SmartPhoneAPI/Account/Login', headers=self.headers, json=json_data)
            self.auth_token = response.json()["UserTokenList"][0]["AuthorizationToken"]
            store.put('auth_token', token=self.auth_token)
        except:
            pass

        return self.auth_token

    def set_car_id(self, car_id):
        self.car_id = car_id

    def check_token(self):
        if self.auth_token:
            return True
        return False

    def start_infinity_park(self):
        headers_temp = {
            'Host': 'app.cellopark-il.com',
            'Authorization': 'Basic '+self.auth_token ,
            'App-Version': '6.65',
            'Device-Os': 'android',
            'Device-Name': 'LGELG-H815',
            'Accept-Language': 'he-IL',
            'App-Key': '12ZsW8HGd9MSAwvg2LAa7izm8DZJi0vk47ux5se7dz0=',
            'Os-Version': '23',
            'User-Agent': 'Device-LGELG-H815,OS-android,App_version-6.65-HUYZNXAHuo5wwpQZpApbmA==',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close',
        }
        print("start_infinity_park startd")

        while(not stop_threads):
            try:
                if not self.car_id:
                    print("no car id!")
                    return
                json_data_start = {'CarNumber': self.car_id,'CityID': 99,'Source': 2,'ZoneID': 59}
                response = requests.post('https://app.cellopark-il.com/SmartPhoneAPI/ParkingSession/ExtendParking',headers=headers_temp,json=json_data_start)
                #print(response.content)
                if "Session" in response.json() and response.json()["Session"]:
                    if "ID" in response.json()["Session"]:
                        self.session_id = response.json()["Session"]["ID"]
                time.sleep(60)
            except Exception as e:
                print(e)
                pass

        print("parking stopped!")

    def stop_parking(self):

        headers_temp = {
            'Host': 'app.cellopark-il.com',
            'Authorization': 'Basic ' + self.auth_token,
            'App-Version': '6.65',
            'Device-Os': 'android',
            'Device-Name': 'LGELG-H815',
            'Accept-Language': 'he-IL',
            'App-Key': '12ZsW8HGd9MSAwvg2LAa7izm8DZJi0vk47ux5se7dz0=',
            'Os-Version': '23',
            'User-Agent': 'Device-LGELG-H815,OS-android,App_version-6.65-HUYZNXAHuo5wwpQZpApbmA==',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close',
        }

        try:
            json_data = {"MethodClose":1,"Source":2,"TransactionID": self.session_id}
            response = requests.post('https://app.cellopark-il.com/SmartPhoneAPI/ParkingSession/StopParking', headers=headers_temp, json=json_data)
        except:
            pass


class MyGrid(GridLayout):
    def __init__(self, **kwargs):

        self.token_label_text = StringProperty()

        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.inside1 = GridLayout()
        self.inside1.cols = 2

        self.inside1.add_widget(Label(text="phone number: "))
        self.phone = TextInput(multiline=False)
        self.inside1.add_widget(self.phone)
        self.add_widget(self.inside1)

        self.submit = Button(text="send sms", font_size=40,background_down="blue")
        self.submit.bind(on_press=self.send_sms)
        self.add_widget(self.submit)


        #####################################################
        ##chek sms
        self.inside2 = GridLayout()
        self.inside2.cols = 2
        self.inside2.add_widget(Label(text="sms code: "))
        self.sms_code = TextInput(multiline=False)
        self.inside2.add_widget(self.sms_code)
        self.add_widget(self.inside2)

        self.get_auth_btn = Button(text="get token", font_size=40)
        self.get_auth_btn.bind(on_press=self.get_auth_btn_func)
        self.add_widget(self.get_auth_btn)

        if cello_api_obj.check_token():
            self.token_label_text = "valid token found!"
            self.token_label_color = [0,1,0,1]
            #self.valid_token = Label(text="valid token found!", font_size=40,color=[0,1,0,1])
        else:
            self.token_label_text = "No token!"
            self.token_label_color = [1,0,0,1]


        self.valid_token = Label(text=self.token_label_text, font_size=40,color=self.token_label_color)

        self.add_widget(self.valid_token)

        ##start parking
        self.inside3 = GridLayout()
        self.inside3.cols = 2
        self.inside3.add_widget(Label(text="car id: "))
        self.car_id = TextInput(multiline=False)
        self.inside3.add_widget(self.car_id)
        self.add_widget(self.inside3)

        self.enable_park = Button(text="enable parking", font_size=40)
        self.enable_park.bind(on_press=self.enable_park_func)
        self.add_widget(self.enable_park)

        self.stop_parking = Button(text="stop parking", font_size=40)
        self.stop_parking.bind(on_press=self.stop_park_func)
        self.add_widget(self.stop_parking)

        self.parking_enabled = Label(text="Paeking is Disable", font_size=40,color=[1,0,0,1])
        self.add_widget(self.parking_enabled)



    def send_sms(self, instance):
        phone = self.phone.text

        cello_api_obj.send_sms(phone)
        print("send sms done")

    def get_auth_btn_func(self, instance):
        phone = self.phone.text
        sms_code = self.sms_code.text

        token = cello_api_obj.verifiy_sms(phone,sms_code)
        if cello_api_obj.check_token():
            self.valid_token = Label(text="valid token found!", font_size=40,color=[0,1,0,1])
        else:
            self.valid_token = Label(text="no token", font_size=40,color=[1,0,0,1])
        print("verifiy_sms done. got token")
        self.token_label_text = "valid token found!"
        self.children[4].text = "valid token found!"
        self.children[4].color = [0,1,0,1]
        self.valid_token.texture_update()

    def enable_park_func(self, instance):
        global stop_threads
        stop_threads = False
        car_id = self.car_id.text
        cello_api_obj.set_car_id(car_id)
        print("starting parking....")
        thread = Thread(target=cello_api_obj.start_infinity_park).start()
        self.children[0].text = "Parking Enabled"
        self.children[0].color = [0,1,0,1]
        self.valid_token.texture_update()

    def stop_park_func(self, instance):
        global stop_threads
        stop_threads = True
        print("stoping parking....")
        cello_api_obj.stop_parking()
        self.children[0].text = "Parking Disabled"
        self.children[0].color = [1,0,0,1]
        self.valid_token.texture_update()


    def stop_just_loolp(self):
        global stop_threads
        stop_threads = True




class MyApp(App):
    def build(self):
        return MyGrid()

cello_api_obj = cell_api()
if __name__ == "__main__":

    MyApp().run()