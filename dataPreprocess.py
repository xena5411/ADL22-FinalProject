import csv 
import json 
import random

def csv_to_array(csvFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)

    return jsonArray

def array_to_dict(array):
    newDict = {}
    for i in array:
        if "course_id" in i:
            newDict[i["course_id"]] = i
        if "user_id" in i:
            newDict[i["user_id"]] = i
        if "subgroup_id" in i:
            newDict[i["subgroup_name"]] = i
        if "group_id" in i:
            newDict[i["group_name"]] = i

    return(newDict)

def array_to_json(array, jsonFilePath):
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(array, indent=4)
        jsonf.write(jsonString)

def MatchUsersAndCourses(courses, users, bought, subgroups,groups):
    returnList = []
    include_user = []
    course_iter = iter(courses)
    for i in bought:
        newDict = {}
        newDict["user_id"] = i["user_id"]
        newDict["b_course_ids"] = i["course_id"].split(" ")
        include_user.append(i["user_id"])
        newDict["b_subgroup_ids"] = []
        newDict["b_group_ids"] = []

        for c_id in newDict["b_course_ids"]:
            subGsOfCourse = courses[c_id]["sub_groups"].split(',') # A list of the subgroups of this course
            GsOfCourse = courses[c_id]["groups"].split(',') # A list of the main groups of this course
            
            for subG in subGsOfCourse:
                if subG != '' and subgroups[subG]["subgroup_id"] not in newDict["b_subgroup_ids"]:
                        newDict["b_subgroup_ids"].append(subgroups[subG]["subgroup_id"])
            for G in GsOfCourse:
                if G != '' and groups[G]["group_id"] not in newDict["b_group_ids"]:
                        newDict["b_group_ids"].append(groups[G]["group_id"])

        usersLikeSubGs = [k.split("_")[1] for k in (users[i["user_id"]]["interests"].split(',')) if len(k.split("_")) > 1]
        newDict["l_subgroup_ids"] =  [subgroups[k]["subgroup_id"] for k in usersLikeSubGs if k in subgroups]
        usersLikeGs = [z.split("_")[0] for z in (users[i["user_id"]]["interests"].split(',')) if len(z.split("_")) > 1]
        newDict["l_group_ids"] = []
        for j in usersLikeGs:
            if j in groups and groups[j]["group_id"] not in newDict["l_group_ids"]:
                newDict["l_group_ids"].append(groups[j]["group_id"])
        

        newDict["l_course_ids"] = []
        newDict["neg_course_ids"] = []
        num = 0
        while True:
            try:
                c_id = next(course_iter)
            except StopIteration:
                course_iter = iter(courses)
                break 
            GsOfCourse = courses[c_id]["groups"].split(',')
            for likeG in usersLikeGs:
                if likeG not in GsOfCourse :
                    newDict["neg_course_ids"].append(c_id)
                    num +=1
                    break
            if num == 10:
                break
        while True:
            try:
                c_id = next(course_iter)
            except StopIteration:
                course_iter = iter(courses)
                break 
            subGsOfCourse = courses[c_id]["sub_groups"].split(',')
            for likeSubG in usersLikeSubGs:
                if likeSubG not in subGsOfCourse :
                    newDict["l_course_ids"].append(c_id)
                    break


        returnList.append(newDict)
        
    for i in users:
        if i not in include_user:
            newDict = {}
            newDict["user_id"] = i
            newDict["b_course_ids"] = []
            newDict["b_subgroup_ids"] = []
            newDict["b_group_ids"] = []
            usersLikeSubGs = [k.split("_")[1] for k in (users[i]["interests"].split(',')) if len(k.split("_")) > 1]
            newDict["l_subgroup_ids"] =  [subgroups[k]["subgroup_id"] for k in usersLikeSubGs if k in subgroups]
            usersLikeGs = [z.split("_")[0] for z in (users[i]["interests"].split(',')) if len(z.split("_")) > 1]
            newDict["l_group_ids"] =[]
            for j in usersLikeGs:
                if j in groups:
                    if groups[j]["group_id"] not in newDict["l_group_ids"]:
                        newDict["l_group_ids"].append(groups[j]["group_id"])
            newDict["l_course_ids"] = []
            newDict["neg_course_ids"] = []
            num = 0
            
            while True:
                try:
                    c_id = next(course_iter)
                except StopIteration:
                    course_iter = iter(courses)
                    break 
                
                GsOfCourse = courses[c_id]["groups"].split(',')
                for likeG in usersLikeGs:
                    if likeG not in GsOfCourse :
                        newDict["neg_course_ids"].append(c_id)
                        num+=1
                        if num > 10:
                            print(num)
                        break
                if num == 10:
                    break
            while True:
                try:
                    c_id = next(course_iter)
                except StopIteration:
                    course_iter = iter(courses)
                    break 
                subGsOfCourse = courses[c_id]["sub_groups"].split(',')
                for likeSubG in usersLikeSubGs:
                    if likeSubG not in subGsOfCourse :
                        newDict["l_course_ids"].append(c_id)
                        break

            
            returnList.append(newDict)




    return returnList


# input
coursesCsvFilePath = r'hahow/data/courses.csv'
usersCsvFilePath = r'hahow/data/users.csv'
usersBuyCoursesCsvFilePath = r'hahow/data/train.csv'
subgroupsDataPath = r'hahow/data/subgroups.csv'
groupsDataPath = r'hahow/data/groups.csv'

#output
jsonFilePath = r'hahow/preprocessed/PosAndNegScore.json'


coursesData = array_to_dict(csv_to_array(coursesCsvFilePath)) # dict
usersData = array_to_dict(csv_to_array(usersCsvFilePath)) # dict
buyData = csv_to_array(usersBuyCoursesCsvFilePath) # list
subgroupsData = array_to_dict(csv_to_array(subgroupsDataPath)) # dict
groupsData = array_to_dict(csv_to_array(groupsDataPath)) # dict

processedData = MatchUsersAndCourses(coursesData, usersData, buyData, subgroupsData, groupsData)

array_to_json(processedData, jsonFilePath)