
pwd=$1
base_path=$2
test_name=$3
partition=$4


export SRUN_ARGS=${SRUN_ARGS}
export PARROTS_BENCHMARK=1

nohup sh runner/seg/train.sh $partition 8 pspnet.benchmark --data_reader MemcachedReader --seed 1024  > /$pwd$base_path$test_name/log_file/seg_pspnet.benchmark 2>&1 &
nohup sh runner/seg/train.sh $partition 8 deeplab.benchmark --data_reader MemcachedReader --seed 1024  > /$pwd$base_path$test_name/log_file/seg_deeplab.benchmark 2>&1 &