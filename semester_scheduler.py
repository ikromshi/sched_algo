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

    students.sort(key=lambda x: x.seniority, reverse=True)


    for day, slots in time_slots.items():
        for time_slot, required in slots:
            if time_slot not in time_slot_map[day]:
                continue  # skip invalid time slots
            slot_index = time_slot_map[day][time_slot]

            # debugging statement
            print(f"Processing {day} at {time_slot}:00 with slot_index {slot_index}")

            available_students = [s for s in students if s.availability[day][slot_index] == "A" and s.assigned_hours < 16]
            available_students.sort(key=lambda x: x.assigned_hours) # is it necessary to sort students

            assigned_count = 0
            while assigned_count < required:
                to_assign = []
                for student in available_students:
                    if assigned_count >= required:
                        break
                    if all(time_slot + i in time_slot_map[day] and student.availability[day][time_slot_map[day][time_slot + i]] == "A" for i in range(2)):  # Ensure at least 2 consecutive hours
                        to_assign.append((student, time_slot))
                        assigned_count += 1

                        # asssign next hour if available
                        if assigned_count < required and time_slot + 1 in time_slot_map[day] and student.availability[day][time_slot_map[day][time_slot + 1]] == "A":
                            to_assign.append((student, time_slot + 1))
                            assigned_count += 1

                # fill remaining slots if needed
                for student in available_students:
                    if assigned_count >= required:
                        break
                    if student.name not in [s.name for s, _ in to_assign] and student.assigned_hours < 16:
                        to_assign.append((student, time_slot))
                        assigned_count += 1

                # Assign students to schedule
                for student, ts in to_assign:
                    if len(schedule[day][ts]) < required and student.name not in schedule[day][ts]:
                        schedule[day][ts].append(student.name)
                        student.assigned_hours += 1
                        student.assigned_shifts[day].append(ts)

                # If we still haven't assigned enough people, move to the next available students
                if assigned_count < required:
                    available_students = [s for s in available_students if s.assigned_hours < 16]

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
    file_path = './data/spring_schedule_upd.csv'
    students = load_students(file_path)
    schedule = create_schedule(students)
    df = pd.DataFrame(schedule).transpose()
    df.columns = ['8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00', '20:00-21:00']
    print(df)
    df.to_csv("./data/output.csv", sep=',')

if __name__ == "__main__":
    main()
