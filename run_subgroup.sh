python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/subgroups.csv \
--coursekey subgroup_id \
--outputkey subgroup \
--bkey b_subgroup_ids_of_course \
--lkey l_subgroup_ids \
--testfile ./hahow/data/test_seen_group.csv \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--model als \
--output ./outputs/test.csv \
--factors 32 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 15 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10.0 \
--l_weight 0 \

# --thresh 0.1 \
# --filter_already_liked_items \

