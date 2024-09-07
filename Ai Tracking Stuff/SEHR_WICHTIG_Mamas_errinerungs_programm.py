# pip install pygame os moviepy

# import time
# from datetime import datetime




# while True:

#     start = input("Do you want to set a reminder? (yes/no): ").lower()

#     survey_finished = False

#     reminder_type = None
#     reminder_timer = None
#     reminder_date = None
#     reminder_message = None


#     if start == "no":
#         pass
#     elif start == "yes":


#        while survey_finished:

#             reminder_type = input("Enter the reminder type ( 'timer' to set a timer, 'date' to remind at a time of day, 'second timer' to be remindet in a certain amount of seconds: ) ")

#             if reminder_type == "timer":
#                 reminder_timer = input("Enter the reminder time (HH:MM) : ")
#                 reminder_timer_int = reminder_timer.split(':')
#                 survey_finished = True
#                 reminder_message = input("Enter the reminder message: ")
#             elif reminder_type == "second timer":
#                 reminder_timer_seconds = input("Enter the reminder time (DON'T REMOVE 0's) SS: ")
#                 reminder_timer_seconds_int = int(reminder_timer_seconds)
#                 survey_finished = True
#                 reminder_message = input("Enter the reminder message: ")
#             elif reminder_type == "date":
#                 reminder_date = input("Enter a time of the day(DON'T REMOVE 0's) HH, MM : ")
#                 survey_finished = True
#                 reminder_message = input("Enter the reminder message: ")
#             else:
#                print(f"{reminder_type} is an Invalid reminder type. Please try again.")
#                survey_finished = False

#        if reminder_type == "timer":

#            reminder_timer_int_list = int(reminder_timer_int[0]) * 3600, int(reminder_timer_int[1]) * 60

#            reminder_timer_int_list_formated = reminder_timer_int_list[0] + reminder_timer_int_list[1] - 1

#            for i in range(reminder_timer_int_list_formated):

#                time.sleep(1)

#            print(f"Reminder: {reminder_message}")
#            break
            
    
#        elif reminder_type == "seconds timer":


#            for i in range(reminder_timer_seconds_int):

#                time.sleep(0.5)

#            print(f"Reminder: {reminder_message}")
#            break
       
import time
from datetime import datetime
import os
import pygame

pygame.mixer.init()
sieren_sound = 'sounds/wiuwiu.mp3'
pygame.mixer.music.load(sieren_sound)
pygame.mixer.music.set_volume(0.)
        
while True:
    start = input("Do you want to set a reminder? (yes/no): ").lower()

    if start == "no":
        break
    elif start == "yes":
        survey_finished = False
        reminder_type = None
        reminder_timer = None
        reminder_date = None
        reminder_message = None

        while not survey_finished:
            reminder_type = input("Enter the reminder type ('timer' to set a timer, 'date' to remind at a time of day, 'second timer' to be reminded in a certain amount of seconds): ")

            if reminder_type == "timer":
                reminder_timer = input("Enter the reminder time (HH:MM): ")
                reminder_timer_int = reminder_timer.split(':')
                survey_finished = True
                reminder_message = input("Enter the reminder message: ")
            elif reminder_type == "second timer":
                reminder_timer_seconds = input("Enter the reminder time (DON'T REMOVE 0's) SS: ")
                reminder_timer_seconds_int = int(reminder_timer_seconds)
                survey_finished = True
                reminder_message = input("Enter the reminder message: ")
            elif reminder_type == "date":
                reminder_date = input("Enter a time of the day (DON'T REMOVE 0's) HH, MM: ")
                survey_finished = True
                reminder_message = input("Enter the reminder message: ")
            else:
                print(f"{reminder_type} is an Invalid reminder type. Please try again.")
                survey_finished = False

        if reminder_type == "timer":
            reminder_timer_int_list = int(reminder_timer_int[0]) * 3600 + int(reminder_timer_int[1]) * 60

            for i in range(reminder_timer_int_list):
                time.sleep(1)
                print(i)

            print(f"Reminder: {reminder_message}")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # pygame.mixer.music.play()
                pygame.time.Clock().tick(10)
                # pygame.mixer.music.play()
            break

        elif reminder_type == "second timer":
            for i in range(reminder_timer_seconds_int):
                time.sleep(1)
                #reminder_timer_seconds_left_int
                print(f"{i} seconds have passed. {reminder_timer_seconds_int - i} seconds left.")

            print(f"Reminder: {reminder_message}")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # pygame.mixer.music.play()
                pygame.time.Clock().tick(10)
                # pygame.mixer.music.play()
            break

        elif reminder_type == "date":
            while reminder_date != datetime.now().strftime("%H, %M"):
                time.sleep(60)
                print("current time:", datetime.now().strftime("%H, %M") )

            print(f"Reminder: {reminder_message}")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                # pygame.mixer.music.play()
                pygame.time.Clock().tick(10)
                # pygame.mixer.music.play()
            break

print(f"exiting...")