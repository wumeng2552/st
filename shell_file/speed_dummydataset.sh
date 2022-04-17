
pwd=$1
base_path=$2
test_name=$3
partition=$4


export SRUN_ARGS=${SRUN_ARGS}
export DUMMYDATASET=1

################################################alphatrion################################################
nohup sh runner/alphatrion/train.sh $partition 8 mobilenet_v2_fp32_benchmark --data_reader MemcachedReader --seed 1024  > /$pwd$base_path$test_name/log_file/alphatrion_mobilenet_v2_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 mobilenet_v2_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_mobilenet_v2_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 se_resnet50_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_se_resnet50_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 se_resnet50_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_se_resnet50_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet50_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet50_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet50_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet50_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet101_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet101_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet101_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet101_fp16_benchmark 2>&1 &
################################################seg_nas################################################
nohup sh runner/seg_nas/train.sh $partition 8 single_path_oneshot --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/seg_nas_single_path_oneshot 2>&1 &
################################################example################################################
nohup sh runner/example/train.sh $partition 8 dpn92_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_dpn92_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 dpn92.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_dpn92.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v4.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v4.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v4_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v4_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet50.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet50.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet50_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet50_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 se_resnet50.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_se_resnet50.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 se_resnet50_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_se_resnet50_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 shuffle_v2.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_shuffle_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 shuffle_v2_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_shuffle_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 mobile_v2.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_mobile_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 mobile_v2_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_mobile_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet18.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet18.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet18_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet18_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet101.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet101.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet101_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet101_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet152.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet152.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet152_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_resnet152_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v2.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v2_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v3.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v3.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v3_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_v3_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_resnet.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_resnet.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_resnet_mix.benchmark --data_reader CephReader --seed 1024 --max_step 1  > /$pwd$base_path$test_name/log_file/example_inception_resnet_mix.benchmark 2>&1 &
