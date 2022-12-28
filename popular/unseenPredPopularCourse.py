import numpy as np
from argparse import ArgumentParser, Namespace
import csv
import json
import random
import codecs
import operator

def main(args):
    random.seed(11)

    allCourse = {}
    
    with open(args.trainFilePath, encoding='utf-8') as f:
        dataset = json.loads(f.read())
    for data in dataset:
        for b_c_id in data['b_course_ids']:
            if b_c_id in allCourse:
                allCourse[b_c_id] += 1
            else:
                allCourse[b_c_id] = 1

    sortedCourses = dict(sorted(allCourse.items(), key=operator.itemgetter(1), reverse=True))
    print(sortedCourses)
    
    populerOutput = []
    for k in sortedCourses:
        if len(populerOutput) < 50:
            populerOutput.append(k)
        else:
            break

    unseenU = []
    with open(args.valFilePath, encoding='utf-8') as f:
        unseenUsers = csv.DictReader(f)
        for user in unseenUsers:
            unseenU.append(user['user_id'])

    with codecs.open(args.predFilePath, "w", "utf8") as o:
        o.write(f'user_id,course_id\n')
        for user in unseenU:
            o.write(f"{user},{' '.join(populerOutput)}\n")
            

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--predFilePath",
        type=str,
        help="pred file path",
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