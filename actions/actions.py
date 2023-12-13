import pymysql
import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionFindFlight(Action):
    def name(self) -> Text:
        return "action_find_flight" #name of customaction

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        destination = tracker.get_slot('destination')
        origin = tracker.get_slot('origin')
        classes = tracker.get_slot('class')
        month = tracker.get_slot('month')

        # Connect to MySQL and retrieve available flights to the destination
        con = pymysql.connect(host='localhost', user='root', password='@rlaalstj0228@', db='rasa3', charset='utf8')
        cur = con.cursor()
        print("connect")

        sql = f"SELECT * FROM flight WHERE destination = '{destination}'AND origin = '{origin}' AND class = '{classes}' AND month = '{month}'"
        cur.execute(sql)
        result = cur.fetchall()

        # flights = [f"Flight ID: {row['flight_id']} | Departure Time: {row['departure_time']}" for row in result]
        flights = [f"Flight ID: {row[0]} | Departure Time: {row[3]} | class : {row[5]}" for row in result]  
        flight_list = ", ".join(flights)
        print(f"Flights: {flights}")
        print(f"Flight List: {flight_list}")
        con.close()

        if len(flights) > 0:
            # 단일 메시지로 출력
            if len(flights) == 1:
                dispatcher.utter_message(text=f"Flight available to {destination} from {origin}: {flight_list}. Would you like to make a reservation?")

            # 복수의 메시지로 반복 출력
            else:
                dispatcher.utter_message(text=f"Flights available to {destination} from {origin}:")
                for flight_info in flights:
                    dispatcher.utter_message(text=f"{flight_info}")
                dispatcher.utter_message(text=f"you choose {classes} class and month : {month}")

        else:
            dispatcher.utter_message(text=f"No flights available from {origin} to {destination}")

        return []

class ActionMakeReservation(Action):
    def name(self) -> Text:
        return "action_make_reservation"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        name = tracker.get_slot('name')
        flight_id = tracker.get_slot('flightid')

        # Connect to MySQL and insert reservation into the database
        con = pymysql.connect(host='localhost', user='root', password='@rlaalstj0228@', db='rasa3', charset='utf8')
        print('reservation-connect')
        cur = con.cursor()

        # # Check if the customer name already exists in the customer table
        # sql_check_customer = f"SELECT * FROM customer WHERE customer_name = '{name}'"
        # cur.execute(sql_check_customer)
        # result = cur.fetchone()

        # if result:
        #     dispatcher.utter_message(text=f"Customer name '{name}' already exists. Please provide a different name.")
        #     return []

        # Check if the flight_id exists in the flight table
        sql_check_flight = f"SELECT * FROM flight WHERE flight_id = '{flight_id}'"
        cur.execute(sql_check_flight)
        result = cur.fetchone()
        print(name)
        print(flight_id)
        if not result:
            dispatcher.utter_message(text=f"Invalid Flight ID: {flight_id}. Please provide a valid Flight ID.")
            return []

        index = random.randint(1, 100)
        sql_reservation = f"INSERT INTO reservation (`reservation_id`, `flight_flight_id`, `customer_customer_name`) VALUES ('{index}', '{flight_id}', '{name}')"

        cur.execute(sql_reservation)
        con.commit()
        print('reservation complete!')
        con.close()


        dispatcher.utter_message(text=f"Reservation made for {name}. Your flight id is {flight_id}")

        return []


class ActionCheckReservation(Action):
   def name(self) -> Text:
      return "action_check_reservation"

   def run(self,
         dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')

        # Connect to MySQL and retrieve reservations for the given customer
        con = pymysql.connect(host='localhost', user='root', password='@rlaalstj0228@', db='rasa3', charset='utf8')
        cur = con.cursor()
        print('check')
        sql = f"SELECT * FROM reservation WHERE customer_customer_name = '{name}'"
        cur.execute(sql)
        result = cur.fetchall()

        if not result:
            dispatcher.utter_message(text=f"No reservations found for {name}.")
        else:
            reservations = [f"Flight ID: {row[1]}" for row in result]
            reservation_list = ", ".join(reservations)
            dispatcher.utter_message(text=f"Reservations for {name}: {reservation_list}")

        con.close()

        return []

class ActionCancelReservation(Action):
    def name(self) -> Text:
        return "action_cancel_reservation"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot('name')
        flight_id = tracker.get_slot('flightid')

        # Connect to MySQL and delete reservation from the database
        con = pymysql.connect(host='localhost', user='root', password='@rlaalstj0228@', db='rasa3', charset='utf8')
        cur = con.cursor()
        
        sql = f"DELETE FROM reservation WHERE customer_customer_name = '{name}' AND flight_flight_id = '{flight_id}'"
        cur.execute(sql)
        con.commit()
        print('delete from reservation table')

        con.close()

        dispatcher.utter_message(text=f"Reservation for {name} on flight {flight_id} canceled.")

        return []
