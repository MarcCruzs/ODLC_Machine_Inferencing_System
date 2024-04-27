#!/bin/bash
#SBATCH --job-name=yolov5_ddp_training
#SBATCH --partition=gpu         # Specify the partition with GPU resources
#SBATCH --nodes=4               # Maximum number of nodes to use
#SBATCH --ntasks-per-node=1     # Number of tasks (processes) to launch per node
#SBATCH --cpus-per-task=32      # Maximum available CPU cores per task
#SBATCH --mem=128G              # Maximum available RAM per node (128G per node, total 512G for 4 nodes)
#SBATCH --gres=gpu:4            # Number of GPUs per node
#SBATCH --time=unlimited        # Runtime set to unlimited

# Change to the directory where your scripts are located
cd /data03/home/marccruz/Github/yolov5

conda activate SUAS

# Run first YOLOv5 script
python -m torch.distributed.run --nproc_per_node=4 train.py --batch 128 --data coco.yaml --weights yolov5s.pt --device 0,1,2,3 --img 640 --epochs 3 \
    --output=yolov5_ddp_output_script1.%j.out --error=yolov5_ddp_output_script1.%j.err

# Run second YOLOv5 script
python -m torch.distributed.run --nproc_per_node=4 train.py --batch 128 --data coco.yaml --weights '' --cfg yolo5s.yaml --device 0,1,2,3 --img 640 --epochs 3 \
    --output=yolov5_ddp_output_script2.%j.out --error=yolov5_ddp_output_script2.%j.err

# Run third YOLOv5 script
python -m torch.distributed.run --nproc_per_node=4 train.py --batch 128 --data coco.yaml --weights yolov5m.pt --device 0,1,2,3 --img 640 --epochs 3 \
    --output=yolov5_ddp_output_script3.%j.out --error=yolov5_ddp_output_script3.%j.err

# Run fourth YOLOv5 script
python -m torch.distributed.run --nproc_per_node=4 train.py --batch 128 --data coco.yaml --weights'' --cfg yolo5s.yaml --device 0,1,2,3 --img 640 --epochs 3 \
    --output=yolov5_ddp_output_script4.%j.out --error=yolov5_ddp_output_script4.%j.err
