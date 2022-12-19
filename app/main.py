from threading import Thread

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import time
import requests
from kivy.storage.jsonstore import JsonStore

store = JsonStore('data.json')



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
        if store.exists('auth_token'):
            self.auth_token =store.get('auth_token')['token']
            if self.auth_token:
                print(self.auth_token)

    def send_sms(self, phone):
        params = {'userName': phone}
        response = requests.get(
            'https://app.cellopark-il.com/SmartPhoneAPI/Account/VerifyPhone',
            params=params,
            headers=self.headers,
        )

    def verifiy_sms(self, phone,sms):
        json_data = {
            'Password': '',
            'SecretCode': sms,
            'UserName': phone,
        }

        response = requests.post('https://app.cellopark-il.com/SmartPhoneAPI/Account/Login', headers=self.headers, json=json_data)
        self.auth_token = response.json()["UserTokenList"][0]["AuthorizationToken"]
        store.put('auth_token', token=self.auth_token)

        return self.auth_token

    def set_car_id(self, car_id):
        self.car_id = car_id

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

        while(1):

            json_data_start = {'CarNumber': self.car_id,'CityID': 99,'Source': 2,'ZoneID': 59}
            response = requests.post('https://app.cellopark-il.com/SmartPhoneAPI/ParkingSession/ExtendParking',headers=headers_temp,json=json_data_start)
            print(response.content)
            time.sleep(60)


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.inside1 = GridLayout()
        self.inside1.cols = 2

        self.inside1.add_widget(Label(text="phone number: "))
        self.phone = TextInput(multiline=False)
        self.inside1.add_widget(self.phone)
        self.add_widget(self.inside1)

        self.submit = Button(text="send sms", font_size=40)
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




    def send_sms(self, instance):
        phone = self.phone.text

        cello_api_obj.send_sms(phone)
        print("send sms done")

    def get_auth_btn_func(self, instance):
        phone = self.phone.text
        sms_code = self.sms_code.text

        token = cello_api_obj.verifiy_sms(phone,sms_code)
        print("verifiy_sms done. got token")

    def enable_park_func(self, instance):
        car_id = self.car_id.text
        cello_api_obj.set_car_id(car_id)
        thread = Thread(target=cello_api_obj.start_infinity_park).start()


class MyApp(App):
    def build(self):
        return MyGrid()

cello_api_obj = cell_api()
if __name__ == "__main__":

    MyApp().run()