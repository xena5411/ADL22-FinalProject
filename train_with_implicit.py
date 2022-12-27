""" An example of using this library to calculate related artists
from the last.fm dataset. More details can be found
at http://www.benfrederickson.com/matrix-factorization/
This code will automatically download a HDF5 version of the dataset from
GitHub when it is first run. The original dataset can also be found at
http://ocelma.net/MusicRecommendationDataset/lastfm-360K.html
"""

import codecs
import logging
import time
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict
import tqdm
import json
import csv
import numpy as np
from scipy.sparse import csr_matrix

from implicit.als import AlternatingLeastSquares
from implicit.approximate_als import (
    AnnoyAlternatingLeastSquares,
    FaissAlternatingLeastSquares,
    NMSLibAlternatingLeastSquares,
)
from implicit.bpr import BayesianPersonalizedRanking
from implicit.datasets.lastfm import get_lastfm
from implicit.lmf import LogisticMatrixFactorization
from implicit.nearest_neighbours import (
    BM25Recommender,
    CosineRecommender,
    TFIDFRecommender,
    bm25_weight,
)

# maps command line model argument to class name
MODELS = {
    "als": AlternatingLeastSquares,
    "nmslib_als": NMSLibAlternatingLeastSquares,
    "annoy_als": AnnoyAlternatingLeastSquares,
    "faiss_als": FaissAlternatingLeastSquares,
    "tfidf": TFIDFRecommender,
    "cosine": CosineRecommender,
    "bpr": BayesianPersonalizedRanking,
    "lmf": LogisticMatrixFactorization,
    "bm25": BM25Recommender,
}

def get_model(args):
    model_name = args.model
    print(f"getting model {model_name}")
    model_class = MODELS.get(model_name)
    if not model_class:
        raise ValueError(f"Unknown Model '{model_name}'")

    # some default params
    if model_name.endswith("als"):
        params = {"dtype": np.float32, "use_gpu": True, "factors": args.factors, "regularization": args.regularization,"alpha": args.alpha, 
        "iterations": args.iterations, "calculate_training_loss": args.calculate_training_loss, "random_state": args.random_state}
    elif model_name == "bm25":
        params = {"K1": args.K1, "B": args.B}
    elif model_name == "bpr":
        params = {"dtype": np.float32, "factors": args.factors, "iterations": args.iterations, "regularization": args.regularization, 
            "random_state": args.random_state, "learning_rate": args.learning_rate}
    elif model_name == "lmf":
        params = {"dtype": np.float32, "factors": args.factors, "iterations": args.iterations, "regularization": args.regularization, 
            "random_state": args.random_state, "learning_rate": args.learning_rate}
    else:
        params = {}

    return model_class(**params)

def main(args):
    # initialize dataset
    # construct a mapping between raw user id and uid
    raw_user_id_to_uid = {}
    uid_to_raw_user_id = []
    with open(args.userfile, encoding='utf-8') as f:
        users = csv.DictReader(f)
        for i, user in enumerate(users):
            raw_user_id_to_uid[user['user_id']] = i
            uid_to_raw_user_id.append(user['user_id'])

    # construct a mapping between raw course id and cid
    raw_course_id_to_cid = {}
    cid_to_raw_course_id = []
    with open(args.coursefile, encoding='utf-8') as f:
        courses = csv.DictReader(f)
        for i, course in enumerate(courses):
            raw_course_id_to_cid[course[args.coursekey]] = i
            cid_to_raw_course_id.append(course[args.coursekey])
    
    # convert the raw user id and course id to uid and cid
    with open(args.trainfile) as f:
        dataset = json.loads(f.read())
    for data in dataset:
        data['user_id'] = raw_user_id_to_uid[data['user_id']]
        data[args.bkey] = [raw_course_id_to_cid[raw_b_course_id] for raw_b_course_id in data[args.bkey]]
        data[args.lkey] = [raw_course_id_to_cid[raw_l_subgroup_to_all_course_id] for raw_l_subgroup_to_all_course_id in data[args.lkey]]

    # construct a sparse matrix
    m_rows = []
    m_cols = []
    m_data = []
    for data in dataset:
        if(args.b_weight > 0):
            for b_course_id in data[args.bkey]:
                # m_cols.append(data['user_id'])
                # m_rows.append(b_course_id)
                m_rows.append(data['user_id'])
                m_cols.append(b_course_id)
                m_data.append(args.b_weight)
        if(args.l_weight > 0):
            for l_course_id in data[args.lkey]:
                # m_cols.append(data['user_id'])
                # m_rows.append(l_course_id)
                m_rows.append(data['user_id'])
                m_cols.append(l_course_id)
                m_data.append(args.l_weight)
    # course_user_matrix = csr_matrix((np.array(m_data), (np.array(m_rows), np.array(m_cols))), shape=(len(cid_to_raw_course_id), len(uid_to_raw_user_id)))
    user_course_matrix = csr_matrix((np.array(m_data), (np.array(m_rows), np.array(m_cols))), shape=(len(uid_to_raw_user_id), len(cid_to_raw_course_id)))

    # create a model from the input data
    model = get_model(args)

    # ******* no bm25 now ******* 
    # # if we're training an ALS based model, weight input for last.fm
    # # by bm25
    # if args.model.endswith("als"):
    #     # lets weight these models by bm25weight.
    #     logging.debug("weighting matrix by bm25_weight")
    #     course_user_matrix = bm25_weight(course_user_matrix, K1=100, B=0.8)

    #     # also disable building approximate recommend index
    #     model.approximate_similar_items = False

    # # this is actually disturbingly expensive:
    # course_user_matrix = course_user_matrix.tocsr()
    # user_course_matrix = course_user_matrix.T.tocsr()

    logging.debug("training model %s", args.model)
    start = time.time()
    model.fit(user_course_matrix)
    logging.debug("trained model '%s' in %0.2fs", args.model, time.time() - start)

    # predict only users in test file
    to_generate = []
    with open(args.testfile, encoding='utf-8') as f:
        testdata = csv.DictReader(f)
        for testdatum in testdata:
            to_generate.append(raw_user_id_to_uid[testdatum['user_id']])

    start = time.time()
    with tqdm.tqdm(total=len(to_generate)) as progress:
        with codecs.open(args.outputfile, "w", "utf8") as o:
            o.write(f'user_id,{args.outputkey}\n')
            for idx in to_generate:
                ids, scores = model.recommend(
                    idx, user_course_matrix[idx], filter_already_liked_items=args.filter_already_liked_items, 
                    N=args.N, recalculate_user=args.recalculate_user,
                )
                user_id = uid_to_raw_user_id[idx]
                # rec_courses = [cid_to_raw_course_id[rec_cid] + '**' + str(score) for rec_cid, score in zip(ids, scores)]
                if args.thresh:
                    rec_courses = [cid_to_raw_course_id[rec_cid] if score > args.thresh else '' for rec_cid, score in zip(ids, scores)]
                else:
                    rec_courses = [cid_to_raw_course_id[rec_cid] for rec_cid in ids]
                o.write(f"{user_id},{' '.join(rec_courses)}\n")
                progress.update(1)
    logging.debug("generated recommendations in %0.2fs", time.time() - start)

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--output",
        type=str,
        default="similar-artists.tsv",
        dest="outputfile",
        help="output file name",
    )
    parser.add_argument(
        "--savemodeldir",
        type=str,
        help="save model dir",
    )
    parser.add_argument(
        "--userfile",
        type=str,
        help="user file name",
    )
    parser.add_argument(
        "--coursefile",
        type=str,
        help="course file name",
    )
    parser.add_argument(
        "--coursekey",
        type=str,
        help="course key name",
    )
    parser.add_argument(
        "--outputkey",
        type=str,
        help="output key name",
    )
    parser.add_argument(
        "--bkey",
        type=str,
        help="bought course key name",
    )
    parser.add_argument(
        "--lkey",
        type=str,
        help="liked course key name",
    )
    parser.add_argument(
        "--testfile",
        type=str,
        help="test file name",
    )
    parser.add_argument(
        "--trainfile",
        type=str,
        help="train file name",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="als",
        dest="model",
        help=f"model to calculate ({'/'.join(MODELS.keys())})",
    )
    parser.add_argument(
        "--factors",
        type=int,
        help="The number of latent factors to compute",
    )
    parser.add_argument(
        "--regularization",
        type=float,
        help="The regularization factor to use",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        help="The learning rate to use",
    )
    parser.add_argument(
        "--K1",
        type=float,
        help="K1 for bm25",
    )
    parser.add_argument(
        "--B",
        type=float,
        help="B for bm25",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        help="The weight to give to positive examples",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        help="The number of ALS iterations to use when fitting data",
    )
    parser.add_argument(
        "--calculate_training_loss",
        help="Whether to log out the training loss at each iteration",
        action='store_true',
    )
    parser.add_argument(
        "--N",
        type=int,
        help="The number of results to return",
    )
    parser.add_argument(
        "--filter_already_liked_items",
        action='store_true',
        help="When true, don't return items present in the training set that were rated by the specified user.",
    )
    parser.add_argument(
        "--recalculate_user",
        action='store_true',
        help="When true, don't rely on stored user embeddings and instead recalculate from the passed in user_items. This option isn't supported by all models.",
    )
    parser.add_argument(
        "--random_state",
        type=int,
        default=None,
        help="The random state for seeding the initial item and user factors. Default is None.",
    )
    parser.add_argument(
        "--b_weight",
        type=float,
        help="The weight to give to bought courses",
    )
    parser.add_argument(
        "--l_weight",
        type=float,
        help="The weight to give to like courses",
    )
    parser.add_argument(
        "--thresh",
        type=float,
        default=0,
        help="The threshhold score",
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    print(args)
    logging.basicConfig(level=logging.DEBUG)
    main(args)