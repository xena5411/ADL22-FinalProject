import numpy as np
from argparse import ArgumentParser, Namespace
import csv
import json
import random
import codecs

def main(args):
    random.seed(11)
    
    unseenU = []
    with open(args.valFilePath, encoding='utf-8') as f:
        unseenUsers = csv.DictReader(f)
        for user in unseenUsers:
            unseenU.append(user['user_id'])
    # unseenU = set(unseenU)

    randomOutput = {}
    with open(args.trainFilePath, encoding='utf-8') as f:
        dataset = json.loads(f.read())
    for data in dataset:
        if data['user_id'] in unseenU:
            random.shuffle(data["l_course_ids"])
            randomOutput[data['user_id']] = data["l_course_ids"][:50]

    
    with codecs.open(args.predFilePath, "w", "utf8") as o:
        o.write(f'user_id,course_id\n')
        for user in unseenU:
            o.write(f"{user},{' '.join(randomOutput[user])}\n")
            

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