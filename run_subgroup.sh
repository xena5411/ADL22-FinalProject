predFilePath="./outputs/lmf/pred_val_seen_subgroup_f64_i100_r06_lr1_b10_l2.csv"
valFile="./hahow/data/val_seen_group.csv"
testFile="./hahow/data/val_seen_group.csv"

CUDA_VISIBLE_DEVICES=3 python train_with_implicit.py \
--userfile ./hahow/data/users.csv \
--coursefile ./hahow/data/subgroups.csv \
--coursekey subgroup_id \
--outputkey subgroup \
--bkey b_subgroup_ids \
--lkey l_subgroup_ids \
--testfile $testFile \
--trainfile ./hahow/preprocessed/PosAndNegScore.json \
--calculate_training_loss \
--output $predFilePath \
--model lmf \
--factors 64 \
--iterations 100 \
--regularization 0.6 \
--learning_rate 1 \
--b_weight 10 \
--l_weight 2 \
--random_state 42 \
--N 50 \

# --K 20 \
# --K1 100 \
# --B 0.1 \
# --alpha 1.0 \
# --thresh 0.1 \
# --filter_already_liked_items \

python matrix.py \
--predFilePath $predFilePath \
--valFilePath $valFile \
--type "subgroup" \



