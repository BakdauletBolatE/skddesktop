import fdb
from datetime import date

today = date.today()
class Ent():
    
    def get_events(self):
        con = fdb.connect(dsn='CBASE.FDB', user='SYSDBA', password='masterkey')
        cur = con.cursor() 
        cur.execute("select * from FB_EVN order by DT")
        events = cur.fetchall()
        return events

    def collect_events(self):
        collect_events = []
        events = self.get_events()
        for event in events:
            unic_id = event[0]
            date = event[1]
            mac_ip = event[2]
            code1 = event[3]
            code2 = event[4]
            if int(code1) == 3 and int(code2) == 0 and mac_ip == '000B3A007AE2':
                code = 1
            elif int(code1) == 3 and int(code2) == 0 and mac_ip == '000B3A007AE3':
                code = 0
            else:
                continue
            
            user_id = event[7]
            con = fdb.connect(dsn='CBASE.FDB', user='SYSDBA', password='masterkey')
            cur = con.cursor() 
            cur.execute(f"select * from FB_USR where id={user_id}")
            user = cur.fetchone()
            iin = user[1]
            surname = user[3]
            name = user[2]
            collect_events.append(
                (
                    unic_id,
                    iin,
                f"{surname} {name}",
                code,
                date.strftime("%d.%m.%Y %H:%M:%S"),
                today
            ))

        return collect_events





