import random
import json
import copy
from collections import OrderedDict
    
def p(string):
    return print(str(string))

def generate_schedule(data):
    schedules = []
    #Generating 30 plans and chosing the best one using gaps points
    for i in range(30):
        schedules.append(generate_one_schedule(data))
    
    the_best_schedule = schedules[0]
    for i in schedules:
        if not "error" in i:
            if i["n_points"]<the_best_schedule["n_points"]:
                the_best_schedule = i
    json_object = json.dumps(the_best_schedule)
    return json_object



def generate_one_schedule(data):

    data  = copy.deepcopy(data)

    school_schedule_dict = {}

    #Gaps points for schedule ranking
    school_schedule_dict["n_points"] = 1000
    gaps = 0
    gap_points = [1,1,10,10,10,10,10,10,10,10]
    gap_point = 0

    #Changing teacher avaiable hours to [] from {}
    for teacher_s in data["teachermodel_set"]:
        hours_set = []
        for hour in teacher_s["avaiable_hours"]:
            hours_set.append(hour["time"])
        teacher_s["avaiable_hours"] = hours_set
        #p(teacher_s["avaiable_hours"])
    
    #Changing class avaiable hours to [] from {}
    for class_s in data["classmodel_set"]:
        hours_set = []
        for hour in class_s["avaiable_hours"]:
            hours_set.append(hour["time"])
        class_s["avaiable_hours"] = hours_set

    #Adding time to the lesson
    for i in data['classmodel_set']:
        random.shuffle(i["lessonmodel_set"])
        for lesson in i["lessonmodel_set"]:
            time=1
            s_class = i
            for t in data['teachermodel_set']:
                if t["id"] == lesson["techer"]:
                    teacher = t
                    
            # most wanted order of lessons
            p_time = [11,21,31,41,51,12,22,32,42,52,13,23,33,43,53,14,24,34,44,54,15,25,35,45,55,16,26,36,46,56,17,27,37,47,57,10,20,30,40,50,18,28,38,48,58,19,29,39,49,59]
            for k in range(50):
                if p_time[k] in teacher["avaiable_hours"] and p_time[k] in s_class["avaiable_hours"]:
                    teacher["avaiable_hours"].remove(p_time[k])
                    s_class["avaiable_hours"].remove(p_time[k])
                    lesson["time"] = p_time[k]
                    break
        
        #checking if all classes have time
        for lesson in i["lessonmodel_set"]:
            if not "time" in lesson:
                school_schedule_dict["error"] = True
                school_schedule_dict["n_points"] = 1000
                school_schedule_dict["source"] = lesson
                school_schedule_dict["teachers"] = data['teachermodel_set']
                return school_schedule_dict

    #Adding lesson to teachers
    school_schedule_dict["teachers"] = []
    for teacher in data['teachermodel_set']:
        teacher_dict = {"id":teacher["id"], "name":teacher["name"],"avaiable_hours":teacher["avaiable_hours"]}
        schedule = []
        for i in data['classmodel_set']:
            for lesson in i["lessonmodel_set"]:
                if lesson["techer"] == teacher["id"]:
                    schedule.append(lesson)
        schedule = sorted(schedule, key = lambda k: k["time"])

        times = []
        day1 = []
        day2 = []
        day3 = []
        day4 = []
        day5 = []
        for lesson in schedule:
            if int(lesson["time"])>=0 and int(lesson["time"])<10:
                day1.append(int(lesson["time"]))
            elif int(lesson["time"])>=10 and int(lesson["time"])<20:
                day2.append(int(lesson["time"]))
            elif int(lesson["time"])>=20 and int(lesson["time"])<30:
                day3.append(int(lesson["time"]))
            elif int(lesson["time"])>=30 and int(lesson["time"])<40:
                day4.append(int(lesson["time"]))
            elif int(lesson["time"]) >=40 and int(lesson["time"])<50:
                day5.append(int(lesson["time"]))
        times.append(day1)
        times.append(day2)
        times.append(day3)
        times.append(day4)
        times.append(day5)
        
        #calculating number of gaps and giving them points
        for day in times:
            if len(day):  
                last = day[0]
                for i in day:
                    if  i == last or i == last+1:
                        pass
                    else:
                        gaps += (i-last-1)
                        gap_point += gap_points[i-last-2]
                    last = i
        
        teacher_dict["lessons"] = schedule
        school_schedule_dict["teachers"].append(teacher_dict) 
    
    gap_points = [10,10,20,30,30,30,30,30,30,30]
    school_schedule_dict["classes"] = []

    #Sorting lessons by time and class
    for i in data['classmodel_set']:
        class_dict = {"id":i["id"], "name":i["name"]}

        schedule = []
        for lesson in i["lessonmodel_set"]:
            if lesson["school_class"] == i["id"]:
                schedule.append(lesson)
        schedule = sorted(schedule, key = lambda k: k["time"])
        class_dict["lessons"] = schedule
        school_schedule_dict["classes"].append(class_dict) 


        times = []
        day1 = []
        day2 = []
        day3 = []
        day4 = []
        day5 = []
        for lesson in schedule:
            if int(lesson["time"])>=0 and int(lesson["time"])<10:
                day1.append(int(lesson["time"]))
            elif int(lesson["time"])>=10 and int(lesson["time"])<20:
                day2.append(int(lesson["time"]))
            elif int(lesson["time"])>=20 and int(lesson["time"])<30:
                day3.append(int(lesson["time"]))
            elif int(lesson["time"])>=30 and int(lesson["time"])<40:
                day4.append(int(lesson["time"]))
            elif int(lesson["time"]) >=40 and int(lesson["time"])<50:
                day5.append(int(lesson["time"]))
        times.append(day1)
        times.append(day2)
        times.append(day3)
        times.append(day4)
        times.append(day5)
        #p(times)

        #calculating schedule points
        for day in times:
            if len(day): 
                last = day[0]
                for i in day:
                    if not i == last and not i == last+1:
                        gaps += (i-last-1)
                        gap_point += gap_points[i-last-2]
                    last = i
    school_schedule_dict["n_points"] = gap_point
    return school_schedule_dict
