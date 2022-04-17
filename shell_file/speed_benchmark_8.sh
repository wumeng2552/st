
pwd=$1
base_path=$2
test_name=$3
partition=$4


export SRUN_ARGS=${SRUN_ARGS}
export PARROTS_BENCHMARK=1

nohup sh runner/seg/train.sh $partition 8 mobilenet_v2_plus.benchmark --data_reader MemcachedReader --seed 1024  > /$pwd$base_path$test_name/log_file/seg_mobilenet_v2_plus.benchmark 2>&1 &
