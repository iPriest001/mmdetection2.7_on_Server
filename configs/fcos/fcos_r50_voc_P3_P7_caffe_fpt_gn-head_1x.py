_base_ = [
    '../_base_/datasets/voc0712.py',
    '../_base_/default_runtime.py'
]
# model settings
model = dict(
    type='FCOS',
    pretrained='open-mmlab://detectron/resnet50_caffe',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=False),
        norm_eval=True,
        style='caffe'),
    neck=dict(
        type='FPT',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=1,  # P3
        add_extra_convs=True,  # use P6-P7
        extra_convs_on_inputs=False,
        num_outs=5,  # in = out
        with_norm='none',  # maybe need to modify 'group_norm' or 'batch_norm'
        upsample_method='bilinear'),
    bbox_head=dict(
        type='FCOSHead',
        num_classes=20,  # change the num of class
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        strides=[8, 16, 32, 64, 128],  # FPT P3-P7
        # strides = [4, 8, 16, 32],
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_bbox=dict(type='IoULoss', loss_weight=1.0),
        loss_centerness=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0)),
    # training and testing settings
    train_cfg=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.5,
            neg_iou_thr=0.4,
            min_pos_iou=0,
            ignore_iof_thr=-1),
        allowed_border=-1,
        pos_weight=-1,
        debug=False),
    test_cfg=dict(
        nms_pre=1000,
        min_bbox_size=0,
        score_thr=0.05,
        nms=dict(type='nms', iou_threshold=0.5),
        max_per_img=100))


data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2)

optimizer = dict(type='SGD', lr=0.00125, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)
# learning policy
# actual epoch = 3 * 3 = 9
lr_config = dict(policy='step', step=[3])
# runtime settings
# total_epochs = 10  # actual epoch = 4 * 3 = 12
# runtime settings
runner = dict(
    type='EpochBasedRunner', max_epochs=8)  # actual epoch = 4 * 3 = 12