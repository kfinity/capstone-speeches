#!/bin/bash
#SBATCH -n 1
#SBATCH -t 01:00:00
#SBATCH -o data/create_records.log
#SBATCH -p standard
#SBATCH -A speech-capstone

# if this script is named "youtube.slurm", schedule it with "sbatch youtube.slurm" 
# it runs at 1am currently
# you can check on the progress with "squeue | grep youtube"

# needed to make sure you have the right environment set up.
module load anaconda

# pull down the videos, save them
python create_records.py

# reschedule for the next day
sbatch youtube.slurm


