import json
import pandas as pd
from collections import defaultdict

class Student:
    def __init__(self, name, seniority, availability):
        self.name = name
        self.seniority = seniority
        self.availability = availability
        self.assigned_hours = 0
        
        # track assigned shifts for consecutive hours
        self.assigned_shifts = defaultdict(list)  

        def __str__(self):
            return self.name


def create_schedule(students):
    '''
    Function to create the entire schedule using a list of student objects with their respective availabilites;
    '''
    # the weekly schedule with required number of workers per time slot
    schedule = defaultdict(lambda: defaultdict(list))
    
    # maps the abstract slot in the algorithm to a specific slot in the schedule
    specify_slot = defaultdict(lambda: defaultdict(str))
    specify_slot["Monday"] = {
            8: "7:55-8:55am",
            9: "8:55-9:55am",
            10: "9:55-10:55am",
            11: "10:55-11:55am",
            12: "11:55-12:55pm",
            13: "12:55-1:55pm",
            14: "1:55-2:55pm",
            15: "2:55-4:00pm",
            16: "4:00-5:00pm",
            17: "5:00-6:00pm",
            18: "6:00-7:00pm",
            19: "7:00-8:00pm",
            20: "8:00-9:00pm"
        }
    specify_slot["Tuesday"] = {
            8: "7:55-9:20am",
            9: "9:20-10:45am",
            10: "10:45-12:10am",
            12: "12:10-1:05pm",
            13: "1:05-2:30pm",
            14: "2:30-3:55pm",
            16: "3:55-5:20pm",
            17: "5:20-6:45pm",
            18: "6:45-8:00pm",
            20: "8:00-10:00pm"
        }
    

    # time slots and required number of workers
    time_slots = {
        'Monday': [
            (8, 2), (9, 3), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 4), (16, 4), (17, 3), (18, 3), (19, 3), (20, 1),
        ],
        'Tuesday': [
            (8, 2), (9, 4), (10, 5), (12, 5), (13, 5), (14, 5), (16, 4), (17, 3), (18, 3), (20, 1),
        ],
        'Wednesday': [
            (8, 2), (9, 3), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 4), (16, 4), (17, 3), (18, 3), (19, 3), (20, 1),
        ],
        'Thursday': [
            (8, 2), (9, 4), (10, 5), (12, 5), (13, 5), (14, 5), (16, 4), (17, 3), (18, 3), (20, 1),
        ],
        'Friday': [
            (8, 2), (9, 3), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 4), (16, 4), (17, 3), (18, 3), (19, 3),
        ],
        'Saturday': [
            (12, 2), (13, 2), (14, 2), (15, 2), (16, 2),
        ],
        'Sunday': [
            (12, 3), (13, 3), (14, 3), (15, 3), (16, 3), (17, 3), (18, 3), (19, 3), (20, 1),
        ]
    }

    time_slot_map = {
        'Monday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12},
        'Tuesday': {8: 0, 9: 1, 10: 2, 12: 3, 13: 4, 14: 5, 16: 6, 17: 7, 18: 8, 20: 9},
        'Wednesday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12},
        'Thursday': {8: 0, 9: 1, 10: 2, 12: 3, 13: 4, 14: 5, 16: 6, 17: 7, 18: 8, 20: 9},
        'Friday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11},
        'Saturday': {12: 0, 13: 1, 14: 2, 15: 3, 16: 4},
        'Sunday': {12: 0, 13: 1, 14: 2, 15: 3, 16: 4, 17: 5, 18: 6, 19: 7, 20: 8}
    }

    assigned_hours_map = defaultdict(lambda: defaultdict(int))
    
    day_slot_person = defaultdict(lambda: defaultdict(list))
    """
    {"monday": {
        "7:55-8:55": ["Ikrom", "Jordan", "Hadil"],
    }}
    """

    # adds a student to a specific shift slot in a day
    def add_student(day, slot, student):
        if day == "Tuesday" or day == "Thursday":
            shift_time = specify_slot['Tuesday'][slot]
            day_slot_person[day][shift_time].append(student.name)
        else:
            shift_time = specify_slot["Monday"][slot]
            day_slot_person[day][shift_time].append(student.name)


    students.sort(key=lambda x: x.seniority, reverse=True)


    for day, slots in time_slots.items():
        for time_slot, required in slots:
            # assigned_hours_map[day][time_slot] = required

            if time_slot not in time_slot_map[day]:
                continue  # skip invalid time slots
            slot_index = time_slot_map[day][time_slot]

            # debugging statement
            # print(f"Processing {day} at {time_slot}:00 with slot_index {slot_index}")

            available_students = [s for s in students if s.availability[day][slot_index] == "A" and s.assigned_hours < 16]
            # available_students.sort(key=lambda x: x.assigned_hours) # is it necessary to sort students

            assigned_hours_map[day][time_slot] = 0
            while assigned_hours_map[day][time_slot] < required:
                to_assign = []
                for student in available_students:
                    if assigned_hours_map[day][time_slot] >= required:
                        break
                    if all(time_slot + i in time_slot_map[day] and student.availability[day][time_slot_map[day][time_slot + i]] == "A" for i in range(2)):  # Ensure at least 2 consecutive hours
                        to_assign.append((student, time_slot))
                        # add_student(day, time_slot, student) # testing day_slot_person
                        assigned_hours_map[day][time_slot] += 1

                        # asssign next hour if available
                        if assigned_hours_map[day][time_slot+1] < time_slots[day][slot_index][1] and time_slot + 1 in time_slot_map[day] and student.availability[day][time_slot_map[day][time_slot + 1]] == "A":
                            to_assign.append((student, time_slot + 1))
                            # add_student(day, time_slot, student) # testing day_slot_person
                            assigned_hours_map[day][time_slot+1] += 1

                # fill remaining slots if needed
                for student in available_students:
                    if assigned_hours_map[day][time_slot] >= required:
                        break
                    if student.name not in [s.name for s, _ in to_assign] and student.assigned_hours < 16:
                        to_assign.append((student, time_slot))
                        # add_student(day, time_slot, student) # testing day_slot_person
                        assigned_hours_map[day][time_slot] += 1

                # Assign students to schedule
                for student, ts in to_assign:
                    if len(schedule[day][ts]) < required and student.name not in schedule[day][ts]:
                        schedule[day][ts].append(student.name)
                        student.assigned_hours += 1
                        student.assigned_shifts[day].append(ts)
                        add_student(day, ts, student) # testing day_slot_person

                # If we still haven't assigned enough people, move to the next available students
                if assigned_hours_map[day][time_slot] < required:
                    available_students = [s for s in available_students if s.assigned_hours < 16]

    formatted_schedule = {day: {time: ', '.join(names) for time, names in times.items()} for day, times in schedule.items()}
    return (formatted_schedule, day_slot_person)

def load_students(file_path):
    df = pd.read_csv(file_path)
    students = []

    for index, row in df.iterrows():
        name = row["Name (First)"]
        seniority = int(row["Seniority"])
        availability = {
            'Monday': row[1:14].tolist(),
            'Tuesday': row[14:24].tolist(),
            'Wednesday': row[24:37].tolist(),
            'Thursday': row[37:47].tolist(),
            'Friday': row[47:59].tolist(),
            'Saturday': row[59:64].tolist(),
            'Sunday': row[64:73].tolist(),
        }
        students.append(Student(name, seniority, availability))
    
    return students

def main():
    file_path = './data/spring_schedule_upd.csv'
    students = load_students(file_path)
    studentsDF = pd.DataFrame(students)
    studentsDF.to_json("./schedule.json")
    schedule, new_schedule = create_schedule(students)
    
    with open("output_json.json", "w") as outfile: 
        json.dump(new_schedule, outfile)

    # print(schedule_df)

if __name__ == "__main__":
    main()
