# python 3.8, Rasa 3.1, MySQL 기반 비행기표 예약 챗봇
## 2023 데이터베이스 체제 실습 Project
## 주제 : 비행기표 예약 챗봇

### Project
 - actions
    - actions.py : custom action programming
- data
    - nlu.yml : Examples that person will write in the chatbot
    - rules.yml : Rules of conversation. We don’t handle it in this class
    - stories.yml : Chatbot’s conversation flow setting
- models : Trained models saved in this folder
- tests : We don’t handle this in this class
- config.yml : Declare basic information of the chatbot
- credentials.yml : We don’t handle this in this class
- domain.yml : Declare intents, entities, actions… etc.
- endpoints.yml : We don’t handle this in this class

### Custom action 
Custom action 을 이용하여 파이썬 코드를 RASA chatbot에서 사용가능하다. 

파이썬 코드에서 pymysql을 import하여 sql query문을 작성하여 데이터를 삽입하거나 삭제한다. 

### mysql
table
- customer
- flight
- reservation

### 실행 방법
rasa run actions -p 5002

rasa shell

### 구현 결과
<img width="686" alt="image" src="https://github.com/minseo0228/Rasa_Chatbot_Customaction/assets/103639821/620546a3-405f-4f3e-a5df-0fe855c56c7f">

[전체 스토리 결과]

![image](https://github.com/minseo0228/Rasa_Chatbot_Customaction/assets/103639821/7f75889c-bc58-4a39-9913-f82a30b562f7)

[비행기표 예약]

비행기표를 예약방식
MySQL DB에 flight 테이블에서 입력한 출발지와 도착지와 동일한 비행기표를 select하여 출력한다.

좌석의 class와 원하는 달을 입력받고 비행기표를 select한다. 

여러 비행기표를 보고 원하는 비행기표 id와 예약자 이름을 넣으면 reservation테이블에 해당 예약정보를 삽입한다. 

![image](https://github.com/minseo0228/Rasa_Chatbot_Customaction/assets/103639821/ec440e80-64ae-4482-a9c7-dd00fc210228)

[예약 확인]

확인하고 싶은 예약자의 이름을 입력하면 reservation 테이블에서 해당이름을 가진 예약 리스트를 출력한다.

![image](https://github.com/minseo0228/Rasa_Chatbot_Customaction/assets/103639821/5a2e7b2e-1fc8-41f4-903e-ab136881e961)

[예약 취소]

취소하고 싶은 예약 정보를 입력하면 reservation db에서 해당 예약 정보를 삭제한다. 


