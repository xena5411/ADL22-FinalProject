python train_with_implicit_subgroup.py \
--testfile ./hahow/data/test_unseen_group.csv \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--model als \
--output ./outputs/pred_test_unseen_group_b10_nl_f32_N50_nf.csv \
--factors 32 \
--regularization 0.05 \
--alpha 1.0 \
--iterations 300 \
--calculate_training_loss \
--random_state 42 \
--N 50 \
--b_weight 10.0 \
--l_weight 1 \

# --thresh 0.1 \
# --filter_already_liked_items \

