import csv 
import json 

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

    return(newDict)

def array_to_json(array, jsonFilePath):
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(array, indent=4)
        jsonf.write(jsonString)

def MatchUsersAndCourses(courses, users, bought, subgroups):
    returnList = []
    include_user = []
    for i in bought:
        newDict = {}
        newDict["user_id"] = i["user_id"]
        newDict["b_course_ids"] = i["course_id"].split(" ")
        include_user.append(i["user_id"])
        for c_id in newDict["b_course_ids"]:
            subGsOfCourse = courses[c_id]["sub_groups"].split(',') # A list of the subgroups of this course
            for subG in subGsOfCourse:
                # the subgroup exists or not
                if subG != '' :
                    if "b_subgroup_ids_of_course" not in newDict:
                        newDict["b_subgroup_ids_of_course"] = [subgroups[subG]["subgroup_id"]]
                    elif subgroups[subG]["subgroup_id"] not in newDict["b_subgroup_ids_of_course"]:
                        newDict["b_subgroup_ids_of_course"].append(subgroups[subG]["subgroup_id"])

        userLikeSubGs = [i.split("_")[1] for i in (users[i["user_id"]]["interests"].split(',')) if len(i.split("_")) > 1]
        newDict["l_subgroup_ids"] =  [subgroups[i]["subgroup_id"] for i in userLikeSubGs if i in subgroups]
        
        newDict["l_subgroup_to_all_course_ids"] = []
        for c_id in courses: 
            subGsOfCourse = courses[c_id]["sub_groups"].split(',')
            for likeSubG in userLikeSubGs:
                if likeSubG in subGsOfCourse and c_id not in newDict["l_subgroup_to_all_course_ids"]:
                    newDict["l_subgroup_to_all_course_ids"].append(c_id)

        
        returnList.append(newDict)
        
    for j in users:
        if j not in include_user:
            newDict = {}
            newDict["user_id"] = j
            newDict["b_course_ids"] = []
            userLikeSubGs = [i.split("_")[1] for i in (users[j]["interests"].split(',')) if len(i.split("_")) > 1]
            newDict["l_subgroup_ids"] =  [subgroups[i]["subgroup_id"] for i in userLikeSubGs if i in subgroups]
            
            newDict["l_subgroup_to_all_course_ids"] = []
            for c_id in courses: 
                subGsOfCourse = courses[c_id]["sub_groups"].split(',')
                for likeSubG in userLikeSubGs:
                    if likeSubG in subGsOfCourse and c_id not in newDict["l_subgroup_to_all_course_ids"]:
                        newDict["l_subgroup_to_all_course_ids"].append(c_id)
            
            returnList.append(newDict)


    return returnList


# input
coursesCsvFilePath = r'hahow/data/courses.csv'
usersCsvFilePath = r'hahow/data/users.csv'
usersBuyCoursesCsvFilePath = r'hahow/data/train.csv'
subgroupsDataPath = r'hahow/data/subgroups.csv'

#output
jsonFilePath = r'hahow/preprocessed/usersAndCourses.json'


coursesData = array_to_dict(csv_to_array(coursesCsvFilePath)) # dict
usersData = array_to_dict(csv_to_array(usersCsvFilePath)) # dict
buyData = csv_to_array(usersBuyCoursesCsvFilePath) # list
subgroupsData = array_to_dict(csv_to_array(subgroupsDataPath)) # dict

processedData = MatchUsersAndCourses(coursesData, usersData, buyData, subgroupsData)
array_to_json(processedData, jsonFilePath)