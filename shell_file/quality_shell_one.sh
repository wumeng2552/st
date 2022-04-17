pwd=$1
base_path=$2
test_name=$3
partition=$4


export SRUN_ARGS=${SRUN_ARGS}
export PARROTS_BENCHMARK=1
################################mmdet########################################################
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_x101_32x4d_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_x101_32x4d_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 faster_rcnn_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_faster_rcnn_r50_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 retinanet_r50_fpn_fp16_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_retinanet_r50_fpn_fp16_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_r101_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_r101_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 cascade_mask_rcnn_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_cascade_mask_rcnn_r50_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_r50_caffe_fpn_mstrain_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_r50_caffe_fpn_mstrain_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_r50_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 cascade_rcnn_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_cascade_rcnn_r50_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_r50_fpn_fp16_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_r50_fpn_fp16_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 retinanet_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_retinanet_r50_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 ssd300_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_ssd300_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 faster_rcnn_r50_fpn_fp16_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_faster_rcnn_r50_fpn_fp16_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 mask_rcnn_x101_64x4d_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_mask_rcnn_x101_64x4d_fpn_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 faster_rcnn_r50_fpn_dconv_c3-c5_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_faster_rcnn_r50_fpn_dconv_c3-c5_1x_coco 2>&1 &
nohup sh runner/mmdet/train.sh $partition 8 fsaf_r50_fpn_1x_coco --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmdet_fsaf_r50_fpn_1x_coco 2>&1 &
#######################################pod#######################################
nohup sh runner/pod/train.sh $partition 8 faster-rcnn-R50-FPN-1x --seed 1024 --max-step 0 --data_reader CephReader > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-R50-FPN-1x 2>&1 &
nohup sh runner/pod/train.sh $partition 8 faster-rcnn-R50-FPN-1x_mix --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-R50-FPN-1x_mix 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 retinanet-R50-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_retinanet-R50-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 mask-rcnn-R50-FPN-1x  --seed 1024 --max-step 0 --data_reader CephReader > /$pwd$base_path$test_name/log_file/pod_mask-rcnn-R50-FPN-1x  2>&1 &
nohup sh runner/pod/train.sh $partition 8 mask-rcnn-R50-FPN-1x_mix --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_mask-rcnn-R50-FPN-1x_mix 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 keypoint-rcnn-R50-FPN-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_keypoint-rcnn-R50-FPN-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 keypoint-rcnn-R50-FPN-1x_mix --seed 1024 --max-step 0 --data_reader CephReader   > /$pwd$base_path$test_name/log_file/pod_keypoint-rcnn-R50-FPN-1x_mix 2>&1 &  
nohup sh runner/pod/train.sh $partition 8 rfcn-R101-ohem-deform-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_rfcn-R101-ohem-deform-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 cascade-rcnn-R50-FPN-1x --seed 1024 --max-step 0 --data_reader CephReader > /$pwd$base_path$test_name/log_file/pod_cascade-rcnn-R50-FPN-1x 2>&1 &
nohup sh runner/pod/train.sh $partition 8 grid-rcnn-R50-FPN-2x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_grid-rcnn-R50-FPN-2x 2>&1 & 
nohup sh runner/pod/train.sh $partition 16 faster-rcnn-R50-NASFPN-1x_mix --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-R50-NASFPN-1x_mix 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 faster-rcnn-mobilenet-FPN-1x --seed 1024 --max-step 0 --data_reader CephReader   > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-mobilenet-FPN-1x 2>&1 &  
nohup sh runner/pod/train.sh $partition 8 faster-rcnn-shufflenet-FPN-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-shufflenet-FPN-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 rfcn-mobilenet-1x --seed 1024 --max-step 0 --data_reader CephReader   > /$pwd$base_path$test_name/log_file/pod_rfcn-mobilenet-1x 2>&1 &  
nohup sh runner/pod/train.sh $partition 8 rfcn-shufflenet-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_rfcn-shufflenet-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 retinanet-R50-ghm-1x --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_retinanet-R50-ghm-1x 2>&1 & 
nohup sh runner/pod/train.sh $partition 8 faster-rcnn-R50-FPN-1x-DCN@C3-C5 --seed 1024 --max-step 0 --data_reader CephReader > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-R50-FPN-1x-DCN@C3-C5 2>&1 &
nohup sh runner/pod/train.sh $partition 8 retinanet-R50-GN-FA --seed 1024 --max-step 0 --data_reader CephReader  > /$pwd$base_path$test_name/log_file/pod_retinanet-R50-GN-FA 2>&1 & 
nohup sh runner/pod/train.sh $partition 16 faster-rcnn-R50-PAFPN-1x_mix --seed 1024 --max-step 0 --data_reader CephReader   > /$pwd$base_path$test_name/log_file/pod_faster-rcnn-R50-PAFPN-1x_mix 2>&1 
#######################################alphatrion#######################################
nohup sh runner/alphatrion/train.sh $partition 8 mobilenet_v2_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_mobilenet_v2_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 mobilenet_v2_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_mobilenet_v2_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 se_resnet50_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_se_resnet50_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 se_resnet50_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_se_resnet50_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet50_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet50_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet50_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet50_fp16_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet101_fp32_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet101_fp32_benchmark 2>&1 &
nohup sh runner/alphatrion/train.sh $partition 8 resnet101_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_resnet101_fp16_benchmark 2>&1 &
#######################################seg_nas#######################################
nohup sh runner/seg_nas/train.sh $partition 8 single_path_oneshot --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/seg_nas_single_path_oneshot 2>&1 &
#######################################ssd#######################################
nohup sh runner/ssd/train.sh $partition 8 ssd_FSAF_benchmark --DATA_READER MemcachedReader --SEED 1024 > /$pwd$base_path$test_name/log_file/ssd_ssd_FSAF_benchmark 2>&1 &
nohup sh runner/ssd/train.sh $partition 8 ssd_Retina_benchmark --DATA_READER MemcachedReader --SEED 1024 > /$pwd$base_path$test_name/log_file/ssd_ssd_Retina_benchmark 2>&1 &
#######################################alphatrion_nas#######################################
nohup sh runner/alphatrion_nas/train.sh $partition 8 super_resnet_range1_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_nas_super_resnet_range1_benchmark 2>&1 &
nohup sh runner/alphatrion_nas/train.sh $partition 8 super_resnet_range1_fp16_benchmark --data_reader MemcachedReader --seed 1024 > /$pwd$base_path$test_name/log_file/alphatrion_nas_super_resnet_range1_fp16_benchmark 2>&1 &
#######################################seg#######################################
nohup sh runner/seg/train.sh $partition 16 pspnet.benchmark --data_reader MemcachedReader > /$pwd$base_path$test_name/log_file/seg_pspnet.benchmark 2>&1 &
nohup sh runner/seg/train.sh $partition 16 deeplab.benchmark --data_reader MemcachedReader > /$pwd$base_path$test_name/log_file/seg_deeplab.benchmark 2>&1 &
nohup sh runner/seg/train.sh $partition 8 mobilenet_v2_plus.benchmark --data_reader MemcachedReader > /$pwd$base_path$test_name/log_file/seg_mobilenet_v2_plus.benchmark 2>&1 &
#######################################example#######################################
nohup sh runner/example/train.sh $partition 8 dpn92_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_dpn92_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 dpn92.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_dpn92.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v4.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v4.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v4_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v4_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet50.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet50.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet50_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet50_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 se_resnet50.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_se_resnet50.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 se_resnet50_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_se_resnet50_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 shuffle_v2.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_shuffle_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 shuffle_v2_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_shuffle_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 mobile_v2.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_mobile_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 mobile_v2_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_mobile_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet18.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet18.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet18_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet18_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet101.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet101.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet101_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet101_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 resnet152.benchmark --data_reader CephReader  > /$pwd$base_path$test_name/log_file/example_resnet152.benchmark 2>&1 & 
nohup sh runner/example/train.sh $partition 8 resnet152_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_resnet152_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v2.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v2.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v2_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v2_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v3.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v3.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_v3_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_v3_mix.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_resnet.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_resnet.benchmark 2>&1 &
nohup sh runner/example/train.sh $partition 8 inception_resnet_mix.benchmark --data_reader CephReader > /$pwd$base_path$test_name/log_file/example_inception_resnet_mix.benchmark 2>&1 &
#######################################mouth#######################################
nohup sh runner/mouth/train.sh $partition 1 v2 --data_reader MemcachedReader --max_step 1 > /$pwd$base_path$test_name/log_file/mouth_v2 2>&1 &
#######################################light_nas#######################################
nohup sh runner/light_nas/train.sh $partition 8 single_path_oneshot_search --max-step 1 > /$pwd$base_path$test_name/log_file/light_nas_single_path_oneshot_search 2>&1 &
#######################################pod_v3.1.0#######################################
nohup sh runner/pod_v3.1.0/train.sh $partition 8 faster-rcnn-R50-FPN-1x --seed 1024 --max-step 0.06  > /$pwd$base_path$test_name/log_file/pod_v3.1.0_faster-rcnn-R50-FPN-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 mask-rcnn-R50-FPN-1x --seed 1024 --max-step 0.06   > /$pwd$base_path$test_name/log_file/pod_v3.1.0_mask-rcnn-R50-FPN-1x 2>&1 & 
nohup sh runner/pod_v3.1.0/train.sh $partition 8 cascade-rcnn-R50-FPN-1x --seed 1024 --max-step 0.06  > /$pwd$base_path$test_name/log_file/pod_v3.1.0_cascade-rcnn-R50-FPN-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 fcos-R50-1x --seed 1024 --max-step 0.06  > /$pwd$base_path$test_name/log_file/pod_v3.1.0_fcos-R50-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 effnetd0-bifpn-retina-32epoch --seed 1024 --max-step 0.2 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_effnetd0-bifpn-retina-32epoch 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 faster-rcnn-R50-FPN-1x-ms-test-aug --seed 1024 --max-step 0.06 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_faster-rcnn-R50-FPN-1x-ms-test-aug 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 grid-rcnn-R50-FPN-2x --seed 1024 --max-step 0.06 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_grid-rcnn-R50-FPN-2x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 keypoint-rcnn-R50-FPN-1x --seed 1024 --max-step 0.1 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_keypoint-rcnn-R50-FPN-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 mask-rcnn-R50-FPN-2x-lvis --seed 1024 --max-step 0.2 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_mask-rcnn-R50-FPN-2x-lvis 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 retinanet-R50-1x --seed 1024 --max-step 0.06 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_retinanet-R50-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 faster-rcnn-R50-FPN-cityscapes --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_faster-rcnn-R50-FPN-cityscapes 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 faster-rcnn-R50-FPN-openimages --seed 1024 --max-step 0.05 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_faster-rcnn-R50-FPN-openimages 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 faster-rcnn-mobilenet-FPN-1x --seed 1024 --max-step 0.05 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_faster-rcnn-mobilenet-FPN-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 rfcn-R101-ohem-deform-1x --seed 1024 --max-step 0.05 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_rfcn-R101-ohem-deform-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 rfcn-shufflenet-1x --seed 1024 --max-step 0.05 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_rfcn-shufflenet-1x 2>&1 &
nohup sh runner/pod_v3.1.0/train.sh $partition 8 centernetkp511-R101-60epoch --seed 1024 --max-step 0.4 > /$pwd$base_path$test_name/log_file/pod_v3.1.0_centernetkp511-R101-60epoch 2>&1 
#######################################mmaction#######################################
nohup sh runner/mmaction/train.sh $partition 8 i3d_r50_video_32x2x1_100e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_i3d_r50_video_32x2x1_100e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 8 r2plus1d_r34_video_8x8x1_180e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_r2plus1d_r34_video_8x8x1_180e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 8 slowfast_r50_video_4x16x1_256e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_slowfast_r50_video_4x16x1_256e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 8 slowonly_r50_video_4x16x1_256e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_slowonly_r50_video_4x16x1_256e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 8 tsm_r50_video_1x1x8_100e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_tsm_r50_video_1x1x8_100e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 8 tsn_r50_video_1x1x8_100e_kinetics400_rgb --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_tsn_r50_video_1x1x8_100e_kinetics400_rgb 2>&1 &
nohup sh runner/mmaction/train.sh $partition 2 bmn_400x100_2x8_9e_activitynet_feature --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmaction_bmn_400x100_2x8_9e_activitynet_feature 2>&1 &
#######################################mmseg#######################################
nohup sh runner/mmseg/train.sh $partition fcn_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_fcn_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition fcn_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_fcn_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ann_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ann_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ann_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ann_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ccnet_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ccnet_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ccnet_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ccnet_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition deeplabv3plus_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500 > /$pwd$base_path$test_name/log_file/mmseg_deeplabv3plus_r101-d8_512x1024_40k_cityscapes 2>&1 & 
nohup sh runner/mmseg/train.sh $partition deeplabv3plus_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_deeplabv3plus_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition deeplabv3_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_deeplabv3_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition deeplabv3_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_deeplabv3_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition encnet_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_encnet_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition encnet_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_encnet_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition fcn_hr18s_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_fcn_hr18s_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition fcn_hr18_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_fcn_hr18_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition gcnet_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_gcnet_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition gcnet_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_gcnet_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition nonlocal_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_nonlocal_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition nonlocal_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_nonlocal_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ocrnet_hr18s_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ocrnet_hr18s_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition ocrnet_hr18_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_ocrnet_hr18_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition psanet_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_psanet_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition psanet_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_psanet_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition pspnet_r101-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_pspnet_r101-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition pspnet_r50-d8_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_pspnet_r50-d8_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition upernet_r101_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_upernet_r101_512x1024_40k_cityscapes 2>&1 &
nohup sh runner/mmseg/train.sh $partition upernet_r50_512x1024_40k_cityscapes --data_reader MemcachedReader --seed 0 --max-step 500> /$pwd$base_path$test_name/log_file/mmseg_upernet_r50_512x1024_40k_cityscapes 2>&1 &