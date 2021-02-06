from pymongo import MongoClient
from datetime import datetime
import sys
import json
client = MongoClient('mongodb://localhost:27017/')
coll = client.attendance.user

today = datetime.today()
now_time = today.strftime('%Y%m')

with open('date.txt', 'r+', encoding='UTF-8') as f:
    if now_time in f:
        pass
    else:
        f.seek(0)
        f.truncate()
        f.write(str(now_time))
        print('-------\n한 달이 지났습니다! =집계 로 출석 횟수 집계 결과를 봐보세요!\n-------')

while True:
    command = input('=출석 <학생이름> : <학생이름> 학생의 출석 횟수를 1회 늘립니다.\n=집계 : 학생들이 이번 한 달에 몇번 출석 했는지 보여줍니다.\n=종료 : 프로그램 종료\n명령어를 입력하세요!')
    if '=출석' in command:
        name = command[4:]
        if coll.find_one({"_id": str(name)}):
            find = {"_id": str(name)}
            setdata = {"$inc": {"count": 1}}
            coll.update_one(find, setdata)
            print(f'-------\n{name} 학생의 정보를 업데이트 했습니다!\n-------')
        else:
            coll.insert_one({"_id": str(name), "count": 1})
            print(f'-------\n{name} 학생의 정보를 DB에 추가 했습니다!\n-------')
            with open('person.txt', 'a', encoding='UTF-8') as files:
                files.write(str(name) + "\n")


    if '=집계' in command:
        ff = open('person.txt', 'r+', encoding='UTF-8')
        for i in ff.readlines():
            i = i.rstrip()
            find_data = coll.find_one({"_id": str(i)})
            da = find_data['_id']
            counts = find_data['count']
            print(f'-------\n{da} 학생의 출석 수 : {counts}')
            set_data = {"$set": {"count": 0}}
            coll.update_one(find_data, set_data)
    if '=종료' in command:
        sys.exit()