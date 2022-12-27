python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/courses.csv \
--coursekey course_id \
--outputkey course_id \
--bkey b_course_ids \
--lkey neg_course_ids \
--testfile ./hahow/data/test_seen.csv \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--model als \
--output ./outputs/pred_test_seen_b10_nl_f64_N50_t02.csv \
--factors 64 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10.0 \
--l_weight 0 \

# --thresh 0.2 \
