import string,random
import requests
import arrow
import sqlite3
from datetime import datetime,date

today = datetime.now()
todayday = date.today()

class IntegrationAonit():

    def __init__(self):
        self.login = 'SKUDUZHSHYM'
        self.password = '123456uzhprod'
        self.con = sqlite3.connect("mydb.db",check_same_thread=False) 
        self.cursor = self.con.cursor()
        self.url = 'http://10.245.12.102:80/bip-sync/?wsdl'
        self.headers = {'content-type': 'application/soap+xml; charset=utf-8'}
        self.dateToBody = arrow.get(datetime.now())

    def sendRequestToAonit(self):
        try:
            response = requests.get(self.url,headers=self.headers)
            dateString = f'{today.day}.{today.month}.{today.year}'
            self.cursor.execute("SELECT * FROM events WHERE created_at = ?;",(todayday,))
            events = self.cursor.fetchall()
          
            def iinIterable():
                string = ''
                for event in events:
                    string += f"<value>{event[1]}</value>"

                return string

            def eventCodeIterable():
                string = ''
                for event in events:
                    string += f"<value>{event[3]}</value>"

                return string

            def datetimeIterable():
                string = ''
                for event in events:
                    string += f"<value>{event[5]} {event[4]}</value>"

                return string


            def testItrable():
                string = ''
                for event in events:
                    string += f"<value>Не задано</value>"

                return string

            body = f"""
                    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <SOAP-ENV:Body>
                <m:SendMessage xmlns:m="http://bip.bee.kz/SyncChannel/v10/Types">
                    <request>
                        <requestInfo>
                            <messageId>String</messageId>
                            <serviceId>EKyzmetUniversalService</serviceId>
                            <messageDate>{self.dateToBody}</messageDate>
                            <sender>
                                <senderId>{self.login}</senderId>
                                <password>{self.password}</password>
                            </sender>
                            <properties>
                                <key></key>
                                <value></value>
                            </properties>
                        </requestInfo>
                        <requestData>
                            <data>
                            <Request serviceName="sendEventFromACSList" xsi:noNamespaceSchemaLocation="EKyzmetUniversalService.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                            <param>
                                <key>ИИН</key>
                                <type>String</type>
                                <values>
                                    {iinIterable()}							
                                </values>
                    
                            </param>
                            <param>
                                <key>Событие</key>
                                <type>String</type>
                                <values>
                                    {eventCodeIterable()}
                                </values>
                            </param>					
                            <param>
                                <key>Время</key>
                                <type>String</type>
                                <values>
                                    {datetimeIterable()}
                                </values>
                            </param>					
                            <param>
                                <key>БИН</key>
                                <type>String</type>
                                <values>
                                    {testItrable()}
                                </values>
                            </param>	
                            <param>
                                <key>Номер этажа</key>
                                <type>String</type>
                                <values>
                                    {testItrable()}
                                </values>
                            </param>
                            <param>
                                <key>Наименование здания</key>
                                <type>String</type>
                                <values>
                                    {testItrable()}
                                </values>
                            </param>												
                        </Request>
                            </data>
                        </requestData>
                    </request>
                </m:SendMessage>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
        """
        
            body = body.encode('utf-8')
            response = requests.post(self.url,data=body, headers=self.headers)
            responseTurple = ""
            if response.status_code == 200:
                responseTurple = (response.status_code, response.text,todayday)
                self.cursor.execute("INSERT INTO responses VALUES (NULL,?,?,?)", responseTurple)
                self.con.commit()
              
                print(f'Сообщение успешно отправлено КОД:{response.status_code}')
                print(response.text)
            else:
                self.cursor.execute("INSERT INTO responses VALUES (NULL,?,?,?)", responseTurple)
                self.con.commit()
               
                print(response.text)
                print(f'Есть ошибка КОД:{response.status_code}')
            return 200
        except requests.exceptions.ConnectionError:
            return 500

      