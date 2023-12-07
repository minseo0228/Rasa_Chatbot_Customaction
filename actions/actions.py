import pymysql
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

        # Connect to MySQL and retrieve available flights to the destination
        con = pymysql.connect(host='localhost', user='root', password='your_password', db='your_db', charset='utf8')
        cur = con.cursor()

        sql = f"SELECT * FROM flights WHERE destination = '{destination}'AND origin = '{origin}'"
        cur.execute(sql)
        result = cur.fetchall()

        flights = [f"Flight ID: {row['flight_id']} | Departure Time: {row['departure_time']}" for row in result]
        flight_list = ", ".join(flights)

        con.close()

        dispatcher.utter_message(text=f"Flights available to {destination}-> {origin} : {flight_list}. Would you like to make a reservation?")

        return []

class ActionMakeReservation(Action):
    def name(self) -> Text:
        return "action_make_reservation"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        origin = tracker.get_slot('origin')
        destination = tracker.get_slot('destination')
        name = tracker.get_slot('name')
        flight_id = tracker.get_slot('flight_id')

        # Connect to MySQL and insert reservation into the database
        con = pymysql.connect(host='localhost', user='root', password='your_password', db='your_db', charset='utf8')
        cur = con.cursor()

        # Assuming 'reservations' table with columns 'origin', 'destination', 'name', and 'flight_id'
        sql = f"INSERT INTO reservations (origin, destination, name, flight_id) VALUES ('{origin}', '{destination}', '{name}', '{flight_id}')"
        cur.execute(sql)
        con.commit()

        con.close()

        dispatcher.utter_message(text=f"Reservation made for {name} from {origin} to {destination}. Your flight id is {flight_id}")

        return []

class ActionCheckReservation(Action):
   def name(self) -> Text:
      return "action_check_reservation"

   def run(self,
         dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot('customer_name')

        # Connect to MySQL and retrieve reservations for the given customer
        con = pymysql.connect(host='localhost', user='root', password='your_password', db='your_db', charset='utf8')
        cur = con.cursor()

        sql = f"SELECT * FROM reservations WHERE customer_name = '{customer_name}'"
        cur.execute(sql)
        result = cur.fetchall()

        if not result:
            dispatcher.utter_message(text=f"No reservations found for {customer_name}.")
        else:
            reservations = [f"Flight ID: {row['flight_id']}" for row in result]
            reservation_list = ", ".join(reservations)
            dispatcher.utter_message(text=f"Reservations for {customer_name}: {reservation_list}")

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
        flight_id = tracker.get_slot('flight_id')

        # Connect to MySQL and delete reservation from the database
        con = pymysql.connect(host='localhost', user='root', password='your_password', db='your_db', charset='utf8')
        cur = con.cursor()

        sql = f"DELETE FROM reservations WHERE name = '{name}' AND flight_id = '{flight_id}'"
        cur.execute(sql)
        con.commit()

        con.close()

        dispatcher.utter_message(text=f"Reservation for {name} on flight {flight_id} canceled.")

        return []
