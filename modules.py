from abc import ABC, abstractmethod
from typing import List
from datetime import datetime, timedelta
import json
import re

class Cinema():
  def __init__(self, name: str, halls:list = [], sсhedule:list = []) -> None:
    self.name = name
    self.halls = halls
    self.sсhedule = sсhedule

  def add_hall(self, hall: 'Hall') -> None:
    self.halls.append(hall)


  def find_hall(self, hall_number: int) -> None:
    for hall in self.halls:
      if hall.number == hall_number:
        return hall
    return 0

  def serialize(self):
    return {"name": self.name, "halls": self.halls, "shedule": self.sсhedule}
    
class Seat():
  def __init__(self, rows: int, number: int) -> None:
    self.row = rows
    self.number = number 
    self.is_reserved = False 

  def serialize(self):
    return {"name": self.name, "halls": self.halls, "shedule": self.sсhedule}

class Hall():
  def __init__(self, number: int, rows: int, seats_per_row: int) -> None:
    self.number = number
    self.rows = rows
    self.schedule = []
    self.seats = [[Seat(row, num) for num in range(1, seats_per_row + 1)] for row in range(1, rows + 1)]

  def add_showtime(self, movie, date_time):
    showtime = Showtime(movie, date_time, self.number, self.seats)
    self.schedule.append(showtime)


  def check_schedule_conflict(self, new_date_time, movie_duration) -> bool:
    for showtime in self.schedule:
      if (new_date_time >= showtime.date_time and new_date_time <= showtime.date_time + timedelta(minutes=movie_duration)):
            return True
    return False



class Movie():
  def __init__(self, name: str, duration: int) -> None:
    self.name = name
    self.duration = duration


class Showtime():
  def __init__(self, movie: Movie, date_time: str, hall_number: int, free_seats: list) -> None:
    self.movie = movie
    self.date_time = date_time
    self.free_seats = free_seats
    self.hall_number = hall_number
    self.tickets = []

  
  def show_free_seats(self):
    for row in self.hall_seats:
      for seat in row:
        if not seat.is_reserved:
          pass

  
  def show_reserved_seats(self):
    print('Забронированные места ->')
    for ticket in self.tickets:
      print(f'Ряд {ticket.seat.row}, Место {ticket.seat.number}')
  
  def get_reserved_seats(self):
    return [ticket.seat for ticket in self.tickets]


  def get_available_showtimes(self, current_time, required_seats, cinema, hall_number) -> List["Showtime"]:
    available_showtimes = []
    for showtime in self.schedule:
      if (showtime.date_time >= current_time and showtime.available_seats >= required_seats):
        available_showtimes.append(showtime)
    return available_showtimes


  def print_seat_plan(self):
        for row in self.hall.seats:
            row_info = ""
            for seat in row:
                if seat.is_reserved:
                    row_info += "X"
                else:
                    row_info += "O"  
            #ЗДесь вывод с пробелами 

class Ticket():
  def __init__(self, showtime: Showtime, seat: Seat):
    self.showtime = showtime
    self.seat = seat

  
  def __str__(self):
        return f"""Информация о билете
        Фильм: {self.showtime.movie.name}
        Кинотеатр: {self.showtime.hall.cinema.name}
        Зал: {self.showtime.hall.number}
        Дата и время: {self.showtime.date_time}
        Место: Ряд {self.seat.row}, Место {self.seat.number}"""
 

  
class System():

  def __init__(self) -> None:
    self.cinemas = []
    

  def find_cinema(self, cinema_name: str) -> None:
    for cinema in self.cinemas:
      if cinema.name == cinema_name:
        return cinema

    return 0

  # def console_print_element(self, filename) -> None:
    
  def add_cinema(self, cinema_name: str) -> None:
    if not self.find_cinema(cinema_name):
      self.cinemas.append(Cinema(cinema_name))

  
  def add_hall(self, cinema_name: str, number: int, seats_per_row: int, rows: int):
    cinema = self.find_cinema(cinema_name)
    if cinema:
      cinema.add_hall(Hall(number, seats_per_row, rows))

  
  def add_showtime(self, movie, cinema_name, hall_number, date_time_str) -> None:
    cinema = self.find_cinema(cinema_name)
    if cinema:
      hall = cinema.find_hall(hall_number)
      if hall:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        if self.check_schedule_conflct(hall_number, date_time, movie.duration):
          raise ValueError("сеанс пересекается с другим")
          hall.add_showtime(movie, date_time)


  def delete_showtime(self, movie, cinema_name: str, hall_number: int, date_time_str, available_seats) -> None:
    cinema = self.find_cinema(cinema_name)
    if cinema:
      hall = cinema.find_hall(hall_number)
      if hall:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        for showtime in hall.shedule:
          hall.schedule.remove(showtime)
          cinema.schedule.remove(showtime)


  def update_showtime(self, cinema_name: str, hall_number: int, date_time_str: str, new_available_seats: int) -> None:
        cinema = self.get_cinema_by_name(cinema_name)
        if cinema:
            hall = cinema.control_hall(hall_number)
            if hall:
                date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                for showtime in self.schedule:
                    if showtime.movie.name == cinema_name and showtime.hall_number == hall_number and showtime.date_time == date_time:
                        showtime.free_seats = new_available_seats
                        return True


  def show_all_showtimes_in_hall(self, cinema_name: str, hall_number: int):
      cinema = self.find_cinema(cinema_name)
      if cinema:
          hall = cinema.control_hall(hall_number)
          if hall:
            return hall.shedule 


  def sell_ticket(self, seat: int, cinema_name : str, hall_number: int, showtime):
    if not seat.is_reserved:
      print('Это место не было заюранировапно')
      ticket = Ticket(self, seat)
      seat.is_resrved = True
      self.aviable_seats -= 1
      self.tickets.append(ticket)
      print('Билет был продан')
      return ticket


class UIManager(ABC): #Абст
  @abstractmethod
  def add_cinema(self, cinema_name: str):
    pass

  @abstractmethod
  def add_hall(self, cinema_name: str, number: int, seats_per_row: int, rows: int):
        pass

  @abstractmethod
  def add_showtime(self, movie, hall_number, date_time_str, available_seats):
        pass

  @abstractmethod
  def check_schedule_conflict(self, hall_number, new_date_time, movie_duration):
        pass

class DataManager(ABC):
  pass
#добавления / удаления / взятие / изменние (4 метода Абстрактных)

class FileManager():
  def __init__(self):
    pass
    
  def save_elements(self, data, filename):
    with open(filename, 'a', encoding='utf-8') as file:
      file.write(str(data.serialize()) + '\n')

  def delete_elements(self, element_to_delete, filename, replacement):
    file_info = ''
    status = input('Напишите, что вы хотите сделать: 1 - Удаление, 2 - Изменение')
    with open(filename, 'r', encoding='utf-8') as file:
      for line in file:
        file_info += line
        pattern = r'^\{.name.\: .<cinema_name>.*\}$'
        if int(status) == 1:
          file_info = re.sub(pattern, '', file_info)
          #добавление в файл
        else:
          input("Какое изменение хотите внести: 1 - ")
          
          
          
        
  

  
    # with open(filename, 'w', encoding='utf-8') as file: 
    #   file.write(file_info)
    

  # def change_elements(self, filename):
  #   with open

#{ 
# "name" : "Kinopark",
# "halls" : [1, 2, 3],
# "schedule" : "chto-to"
# }
    
  def load_elements(self, filename):
    try:
      with open(filename, 'r', encoding='utf-8') as file:
        self.cinemas = json.load(file)
    except FileNotFoundError:
      return False
  
# file_manager = FileManager()
# cinema = Cinema("Monkey", [1, 2, 3], {1: "Time"})

# file_manager.save_elements(cinema, "cinemas.pkl")
# file_manager.load_elements("cinemas.pkl")
# print(file_manager.cinemas)

