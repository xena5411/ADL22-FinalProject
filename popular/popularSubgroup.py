import numpy as np
from argparse import ArgumentParser, Namespace
import csv
import json
import random
import codecs
import operator

def csv_to_dict(csvFilePath):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
        for row in csvReader: 
            jsonArray.append(row)

    newDict = {}
    for i in jsonArray:
        if "course_id" in i:
            newDict[i["course_id"]] = i
        if "subgroup_id" in i:
            newDict[i["subgroup_name"]] = i

    return(newDict)

def main(args):
    random.seed(11)

    coursesCsvFilePath = '../hahow/data/courses.csv'
    subgroupsDataPath = '../hahow/data/subgroups.csv'

    courses_id_to_data = csv_to_dict(coursesCsvFilePath)
    subgroups_name_to_id = csv_to_dict(subgroupsDataPath)
    
    popCourseRank = [] # [c1, c2, ...]
    with open(args.rankFilePath, encoding='utf-8') as f:
        csvReader = csv.reader(f)
        for i in csvReader:
            popCourseRank.append(i[0])

    subGSorted = {} # {"subG_id": [c1, c2, ...]}
    for c in popCourseRank:
        sgs_name_of_c = courses_id_to_data[c]["sub_groups"].split(",")
        for sg_name in sgs_name_of_c:
            if sg_name in subgroups_name_to_id:
                if subgroups_name_to_id[sg_name]["subgroup_id"] not in subGSorted:
                    subGSorted[subgroups_name_to_id[sg_name]["subgroup_id"]] = [c]
                else:
                    subGSorted[subgroups_name_to_id[sg_name]["subgroup_id"]].append(c)
    

    unseenU = [] # ["u_id1", "u_id2", ...]
    with open(args.valFilePath, encoding='utf-8') as f:
        unseenUsers = csv.DictReader(f)
        for user in unseenUsers:
            unseenU.append(user['user_id'])
        
    user_l_subG = {} # {"unseen_user_id": [sG_id1, sG_id2, ...]}
    with open(args.trainFilePath, encoding='utf-8') as f:
        dataset = json.loads(f.read())
    for data in dataset:
        if data['user_id'] in unseenU:
            user_l_subG[data['user_id']] = data["l_subgroup_ids"]
    

    with codecs.open(args.predFilePath, "w", "utf8") as o:
        o.write(f'user_id,course_id\n')
        for u_id in unseenU:
            popCourse = popCourseRank[:5]
            # popCourse = []
            for sg_id in user_l_subG[u_id]:
                popCourse += subGSorted[sg_id][:2]
                if len(popCourse) >= 14:
                    break

            popCourse = list(set(popCourse))
            for c in popCourseRank:
                if len(popCourse) >= 50:
                    break
                elif c not in popCourse:
                    popCourse.append(c)
            
            o.write(f"{u_id},{' '.join(popCourse)}\n")
            

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--predFilePath",
        type=str,
        help="pred file path",
    )
    parser.add_argument(
        "--rankFilePath",
        type=str,
        help="rank file path",
    )
    parser.add_argument(
        "--trainFilePath",
        type=str,
        help="train file path",
    )
    parser.add_argument(
        "--valFilePath",
        type=str,
        help="val file path",
    )
    parser.add_argument(
        "--type",
        type=str,
        help="course_id or subgroup",
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)