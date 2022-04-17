pwd=$1
base_path=$2
test_name=$3
partition=$4


export SRUN_ARGS=${SRUN_ARGS}
export PARROTS_BENCHMARK=1


#######################################mmediting#######################################
nohup sh runner/mmediting/train.sh $partition 1 cyclegan_lsgan_id0_resnet_in_1x1_246200_summer2winter --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_cyclegan_lsgan_id0_resnet_in_1x1_246200_summer2winter 2>&1 &
nohup sh runner/mmediting/train.sh $partition 8 deepfillv2_256x256_8x2_celeba --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_deepfillv2_256x256_8x2_celeba 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 dim_stage2_v16_pln_1x1_1000k_comp1k --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_dim_stage2_v16_pln_1x1_1000k_comp1k 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 edsr_x2c64b16_g1_300k_div2k --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_edsr_x2c64b16_g1_300k_div2k 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 esrgan_psnr_x4c64b23g32_g1_1000k_div2k --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_esrgan_psnr_x4c64b23g32_g1_1000k_div2k 2>&1 &
nohup sh runner/mmediting/train.sh $partition 8 gl_256x256_8x12_celeba --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_gl_256x256_8x12_celeba 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 indexnet_mobv2_1x16_78k_comp1k --data-reader MemcachedReader --seed 1024 --max-step 500  > /$pwd$base_path$test_name/log_file/mmediting_indexnet_mobv2_1x16_78k_comp1k 2>&1 & 
nohup sh runner/mmediting/train.sh $partition 1 msrresnet_x4c64b16_g1_1000k_div2k --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_msrresnet_x4c64b16_g1_1000k_div2k 2>&1 &
nohup sh runner/mmediting/train.sh $partition 8 pconv_256x256_stage1_8x1_celeba --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_pconv_256x256_stage1_8x1_celeba 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 pix2pix_vanilla_unet_bn_1x1_80k_facades --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_pix2pix_vanilla_unet_bn_1x1_80k_facades 2>&1 &
nohup sh runner/mmediting/train.sh $partition 1 srcnn_x4k915_g1_1000k_div2k --data-reader MemcachedReader --seed 1024 --max-step 500 > /$pwd$base_path$test_name/log_file/mmediting_srcnn_x4k915_g1_1000k_div2k 2>&1 &
#######################################TextRecog#######################################
nohup sh runner/TextRecog/train.sh $partition  16 print_Middle --datareader MemcachedReader > /$pwd$base_path$test_name/log_file/TextRecog_print_Middle 2>&1 &
nohup sh runner/TextRecog/train.sh $partition  16 print_Big --datareader MemcachedReader > /$pwd$base_path$test_name/log_file/TextRecog_print_Big 2>&1 &
nohup sh runner/TextRecog/train.sh $partition  16 print_MiddleV2 --datareader MemcachedReader > /$pwd$base_path$test_name/log_file/TextRecog_print_MiddleV2 2>&1 &
nohup sh runner/TextRecog/train.sh $partition  16 crnn --datareader MemcachedReader > /$pwd$base_path$test_name/log_file/TextRecog_crnn 2>&1 &
#######################################mmpose#######################################
nohup sh runner/mmpose/train.sh $partition 8 bottomup_hrnet --data_reader CephReader --seed 1024 --max-step 1 --batch-size 6 > /$pwd$base_path$test_name/log_file/mmpose_bottomup_hrnet 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_alexnet --data_reader CephReader --seed 1024 --max-step 1   > /$pwd$base_path$test_name/log_file/mmpose_topdown_alexnet 2>&1 &  
nohup sh runner/mmpose/train.sh $partition 8 topdown_darkpose --data_reader CephReader --seed 1024 --max-step 1  > /$pwd$base_path$test_name/log_file/mmpose_topdown_darkpose 2>&1 & 
nohup sh runner/mmpose/train.sh $partition 8 topdown_hourglass --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_hourglass 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_hrnet --data_reader CephReader --seed 1024 --max-step 1 --batch-size 32 > /$pwd$base_path$test_name/log_file/mmpose_topdown_hrnet 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_mobilev2 --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_mobilev2 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_res50 --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_res50 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_resnetv1d --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_resnetv1d 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_resnext --data_reader CephReader --seed 1024 --max-step 1  > /$pwd$base_path$test_name/log_file/mmpose_topdown_resnext 2>&1 & 
nohup sh runner/mmpose/train.sh $partition 8 topdown_scnet --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_scnet 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_senet50 --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_senet50 2>&1 &
nohup sh runner/mmpose/train.sh $partition 8 topdown_shufflev1 --data_reader CephReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/mmpose_topdown_shufflev1 2>&1 &
#######################################sketch#######################################
nohup sh runner/sketch/train.sh $partition 8 vgg1.4.3 --max-step 1 > /$pwd$base_path$test_name/log_file/sketch_vgg1.4.3 2>&1 &
nohup sh runner/sketch/train.sh $partition 8 mobilenet1.0.0 --max-step 1 > /$pwd$base_path$test_name/log_file/sketch_mobilenet1.0.0 2>&1 &
nohup sh runner/sketch/train.sh $partition 8 vggfusion --max-step 1 > /$pwd$base_path$test_name/log_file/sketch_vggfusion 2>&1 &
#######################################mmtrack#######################################
nohup sh runner/mmtrack/train.sh $partition 8 config13ms_bn1 --seed 1024 --max_step 2 > /$pwd$base_path$test_name/log_file/mmtrack_config13ms_bn1 2>&1 &
nohup sh runner/mmtrack/train.sh $partition 8 config1ms_lr --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmtrack_config1ms_lr 2>&1 &
nohup sh runner/mmtrack/train.sh $partition 8 siamrpnpp --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmtrack_siamrpnpp 2>&1 &

#######################################RetinaUnet#######################################
nohup sh runner/RetinaUnet/train.sh $partition 1 2d_runet_infer --seed 1024 > /$pwd$base_path$test_name/log_file/RetinaUnet_2d_runet_infer 2>&1 &
#######################################pod_v2.3.0#######################################
nohup sh runner/pod_v2.3.0/train.sh $partition retinanet-v11-18w --data-reader CephReader --seed 1024 --max-step 0.1 > /$pwd$base_path$test_name/log_file/pod_v2.3.0_retinanet-v11-18w 2>&1 &
nohup sh runner/pod_v2.3.0/train.sh $partition fcos-v11-80w-stride4 --data-reader CephReader --seed 1024 --max-step 0.2 > /$pwd$base_path$test_name/log_file/pod_v2.3.0_fcos-v11-80w-stride4 2>&1 &
#######################################pod_v3.0#######################################
nohup sh runner/pod_v3.0/train.sh $partition 8 mask-rcnn-R152-FPN-1x-h --seed 1024 --data_reader CephReader --max_step 1 > /$pwd$base_path$test_name/log_file/pod_v3.0_mask-rcnn-R152-FPN-1x-h 2>&1 &
#######################################prototype#######################################
nohup sh runner/prototype/train.sh $partition 16 resnet50 --seed 1024 --max-step 4000 --data_reader CephReader > /$pwd$base_path$test_name/log_file/prototype_resnet50 2>&1 &
nohup sh runner/prototype/train.sh $partition 16 shufflev2 --seed 1024 --max-step 4000 --data_reader CephReader > /$pwd$base_path$test_name/log_file/prototype_shufflev2 2>&1 &
#######################################encoder#######################################
nohup sh runner/encoder/train.sh $partition 1 benign --max_step 1 > /$pwd$base_path$test_name/log_file/encoder_benign 2>&1 &
#######################################sensemedical#######################################
nohup sh runner/sensemedical/train.sh $partition 8 Task01_BrainTumour --max_step 1 > /$pwd$base_path$test_name/log_file/sensemedical_Task01_BrainTumour 2>&1 &
######################################Pattern#######################################
nohup sh runner/Pattern/train.sh $partition 8 attribute_config --seed 1024 --data_reader ceph --max_step 300 > /$pwd$base_path$test_name/log_file/Pattern_attribute_config --seed 1024 --data_reader ceph --max_step 300  2>&1 &
nohup sh runner/Pattern/train.sh $partition 8 eye_best_config_parrots --seed 1024 --data_reader ceph --max_step 300 > /$pwd$base_path$test_name/log_file/Pattern_eye_best_config_parrots --seed 1024 --data_reader ceph --max_step 300  2>&1 &
nohup sh runner/Pattern/train.sh $partition 8 example_fusion_small_pytorch --seed 1024 --data_reader ceph --max_step 300 > /$pwd$base_path$test_name/log_file/Pattern_example_fusion_small_pytorch --seed 1024 --data_reader ceph --max_step 300  2>&1 &
nohup sh runner/Pattern/train.sh $partition 8 gaze_example --seed 1024 --data_reader ceph --max_step 300 > /$pwd$base_path$test_name/log_file/Pattern_gaze_example --seed 1024 --data_reader ceph --max_step 300  2>&1 &
#######################################instance_seg#######################################
nohup sh runner/instance_seg/train.sh $partition 1 yolact_mobilenetv2_concat_32_coco_config --data-reader CephReader --seed 1024 --max-step 201 > /$pwd$base_path$test_name/log_file/instance_seg_yolact_mobilenetv2_concat_32_coco_config 2>&1 &
#######################################detr#######################################
nohup sh runner/detr/train.sh $partition 8 detr --data_reader CephReader --max_step 1 --seed 42 > /$pwd$base_path$test_name/log_file/detr_detr 2>&1 &
#######################################sr_v3.0#######################################
nohup sh runner/sr_v3.0_0/train.sh $partition 1 F4_0_300 --data_reader MemcachedReader --seed 1024 --max-step 1 > /$pwd$base_path$test_name/log_file/sr_v3.0_0_F4_0_300 2>&1 &
#######################################heart_seg#######################################
nohup sh runner/heart_seg/train.sh $partition  1 resvnet --data_reader MemcachedReader --seed 1024 --max_step 10 > /$pwd$base_path$test_name/log_file/heart_seg_resvnet 2>&1 &
#######################################coronary_seg#######################################
nohup sh runner/coronary_seg/train.sh $partition 1 resvnet --data_reader MemcachedReader --seed 1024 --max_step 10 > /$pwd$base_path$test_name/log_file/coronary_seg_resvnet 2>&1 &
#######################################mmdetection3d#######################################
nohup sh runner/mmdetection3d/train.sh $partition 8 votenet_16x8_sunrgbd-3d-10class --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_votenet_16x8_sunrgbd-3d-10class 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 8 votenet_8x8_scannet-3d-18class --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_votenet_8x8_scannet-3d-18class 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 2 hv_second_secfpn_6x8_80e_kitti-3d-3class --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_second_secfpn_6x8_80e_kitti-3d-3class 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 2 hv_second_secfpn_6x8_80e_kitti-3d-car --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_second_secfpn_6x8_80e_kitti-3d-car 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 8 hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-3class --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-3class 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 8 hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-car --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_PartA2_secfpn_2x8_cyclic_80e_kitti-3d-car 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 8 hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class 2>&1 &
nohup sh runner/mmdetection3d/train.sh $partition 8 hv_pointpillars_secfpn_6x8_160e_kitti-3d-car --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/mmdetection3d_hv_pointpillars_secfpn_6x8_160e_kitti-3d-car 2>&1 &
#######################################deformable_detr#######################################
nohup sh runner/deformable_detr/train.sh $partition 8 r50_deformable_detr_plus_iterative_bbox_refinement_plus_plus_two_stage --data_reader CephReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/deformable_detr_r50_deformable_detr_plus_iterative_bbox_refinement_plus_plus_two_staget 2>&1 &
######################################pattern_v2_5_sp#######################################
nohup sh runner/pattern_v2_5_sp/train.sh $partition  8, V2_6_sp_cos_pretrain_honda, --max_step 320 --seed 100 --pavi --pavi-project pat_weekly_modeltest > /$pwd$base_path$test_name/log_file/pattern_v2_5_sp_V2_6_sp_cos_pretrain_honda 2>&1 &
#######################################PAR#######################################
nohup sh runner/PAR/train.sh $partition 8, res101, --max_step 1 --seed 1024 > /$pwd$base_path$test_name/log_file/PAR_res101 2>&1 &
#######################################Multi_organ_seg_HR#######################################
nohup sh runner/Multi_organ_seg_HR/train.sh $partition 4, PSPNet, --data_reader LustreReader --seed 1024 --max_step 1 > /$pwd$base_path$test_name/log_file/Multi_organ_seg_HR_PSPNet 2>&1 &
#######################################mmocr#######################################
nohup sh runner/mmocr/train.sh $partition 8, panet_r18_fpem_ffm_sbn_1x_ctw1500, --seed 1024 --max_step 5 > /$pwd$base_path$test_name/log_file/mmocr_panet_r18_fpem_ffm_sbn_1x_ctw1500 2>&1 &
nohup sh runner/mmocr/train.sh $partition 8, panet_r18_fpem_ffm_sbn_1x_icdar2015, --seed 1024 --max_step 5 > /$pwd$base_path$test_name/log_file/mmocr_panet_r18_fpem_ffm_sbn_1x_icdar2015 2>&1 &
nohup sh runner/mmocr/train.sh $partition 8, psenet_r50_fpnf_sbn_1x_icdar2015, --seed 1024 --max_step 5 > /$pwd$base_path$test_name/log_file/mmocr_psenet_r50_fpnf_sbn_1x_icdar2015 2>&1 &
nohup sh runner/mmocr/train.sh $partition 8, psenet_r50_fpnf_sbn_1x_ctw1500, --seed 1024 --max_step 5 > /$pwd$base_path$test_name/log_file/mmocr_psenet_r50_fpnf_sbn_1x_ctw1500 2>&1 &
#######################################Crowd#######################################3
nohup sh runner/Crowd/train.sh $partition 8, vgg_csr, --data_reader CephReader --seed 1024 > /$pwd$base_path$test_name/log_file/Crowd_vgg_csr 2>&1 &
nohup sh runner/Crowd/train.sh $partition 8, vgg_sfa, --data_reader CephReader --seed 1024 > /$pwd$base_path$test_name/log_file/Crowd_vgg_csr 2>&1 &
#######################################SenseStar#######################################
nohup sh runner/SenseStar/train.sh $partition 8, sensestar, --data_reader CephReader --seed 1024 --max_step 1 --pavi --pavi_project default > /$pwd$base_path$test_name/log_file/SenseStar_sensestar 2>&1 &
#######################################springce_psot#######################################
nohup sh runner/springce_psot/train.sh $partition 8, vot_non_siam, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_non_siam 2>&1 &
nohup sh runner/springce_psot/train.sh $partition 8, vot_res50-dilation-multirpn, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_res50-dilation-multirpn 2>&1 &
nohup sh runner/springce_psot/train.sh $partition 8, vot_res50-interp-multirpn-focal_loss, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_res50-interp-multirpn-focal_loss 2>&1 &
nohup sh runner/springce_psot/train.sh $partition 8, vot_res50-interp-multirpn-focal_loss-atss, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_res50-interp-multirpn-focal_loss-atss 2>&1 &
nohup sh runner/springce_psot/train.sh $partition 8, vot_res50-interp-multirpn-focal_loss-atss-smoothl1, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_res50-interp-multirpn-focal_loss-atss-smoothl1 2>&1 &
nohup sh runner/springce_psot/train.sh $partition 8, vot_res50-interp-multirpn-focal_loss-topk, --seed 1024 --max_step 0.3 > /$pwd$base_path$test_name/log_file/springce_psot_vot_res50-interp-multirpn-focal_loss-topk 2>&1 &
#######################################mmocr_ctc#######################################
nohup sh runner/mmocr_ctc/train.sh $partition 4, icdar2013_ctc, --seed 1024 --data_reader CephReader --max_step 5 > /$pwd$base_path$test_name/log_file/mmocr_ctc_icdar2013_ctc 2>&1 &
#######################################vision_transformer#######################################
nohup sh runner/vision_transformer/train.sh $partition 8  b16  --seed 1024 --data_reader CephReader --max_step 1 > /$pwd$base_path$test_name/log_file/vision_transformer_b16 2>&1 &
