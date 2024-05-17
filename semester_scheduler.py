import pandas as pd
from collections import defaultdict

class Student:
    def __init__(self, name, seniority, availability):
        self.name = name
        self.seniority = seniority
        self.availability = availability
        self.assigned_hours = 0

# function to create the schedule;
def create_schedule(students):
    # define the weekly schedule with required number of workers per time slot;
    schedule = defaultdict(lambda: defaultdict(list))
    
    # define time slots with required number of workers;
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
    # mapping time slots to availability list indices
    time_slot_map = {
        'Monday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12},
        'Tuesday': {8: 0, 9: 1, 10: 2, 12: 3, 13: 4, 14: 5, 16: 6, 17: 7, 18: 8, 20: 9},
        'Wednesday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11, 20: 12},
        'Thursday': {8: 0, 9: 1, 10: 2, 12: 3, 13: 4, 14: 5, 16: 6, 17: 7, 18: 8, 20: 9},
        'Friday': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 6, 15: 7, 16: 8, 17: 9, 18: 10, 19: 11},
        'Saturday': {12: 0, 13: 1, 14: 2, 15: 3, 16: 4},
        'Sunday': {12: 0, 13: 1, 14: 2, 15: 3, 16: 4, 17: 5, 18: 6, 19: 7, 20: 8}
    }

    # sort students by seniority;
    students.sort(key=lambda x: x.seniority, reverse=True)

    # assign shifts to students
    for day, slots in time_slots.items():
        for time_slot, required in slots:
            slot_index = time_slot_map[day][time_slot]
            available_students = [s for s in students if s.availability[day][slot_index] == "A" and s.assigned_hours < 16]
            available_students.sort(key=lambda x: x.assigned_hours)

            # make sure to assign consecutive hours

            for student in available_students[:required]:
                schedule[day][time_slot].append(student.name)
                student.assigned_hours += 1
    formatted_schedule = {day: {time: ', '.join(names) for time, names in times.items()} for day, times in schedule.items()}

    return formatted_schedule


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
    _file_path = "./spring_schedule_upd.csv"


    students = load_students(_file_path)
    schedule = create_schedule(students)
    df = pd.DataFrame(schedule).transpose()
    print(df)
    df.to_csv("output.csv", sep=',')



if __name__ == "__main__":
    main()
