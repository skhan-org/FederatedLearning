python3  -u main.py --dataset=$1 \
            --optimizer=$2 \
            --learning_rate=0.1 \
            --num_rounds=$3 \
            --eval_every=10 \
            --clients_per_round=10 \
            --batch_size=$4 \
            --q=0 \
	      --seed=0 \
            --model=$5 \
	      --sampling=2  \
            --num_corrupted=$6 \
            --boosting=$7 \
            --random_updates=$8 \
            --gradient_clipping=0 \
            --krum=0 \
            --mkrum=0 \
            --median=0 \
            --k_norm=0 \
            --k_loss=0 \
            --fedmgda=0 \
            --fedmgda_eps=0 \
            --alpha=0 \
            --global_reg=-1 \
            --lam=1 \
            --dynamic_lam=0 \
            --finetune_iters=40 \
            --decay_factor=1 \
            --local_iters=2 \
		> $9