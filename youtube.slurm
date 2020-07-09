#!/bin/bash
#SBATCH -n 1
#SBATCH -t 01:00:00
#SBATCH -o yt_speeches.out
#SBATCH -p standard
#SBATCH -A mygroup

module load anaconda3

# pull down the videos, write them to mongodb
python youtube_automation.py

# reschedule for the next day
sbatch youtube.slurm
