#!/bin/bash -l
#$ -S /bin/bash
#$ -P RCSoftDev
#$ -l h_rt=1:0:0
#$ -l mem=16G
#$ -N Newsrods
#$ -pe mpi 16
#$ -l paid=1
#$ -ac allow="U"
#$ -wd /home/ccearal/Scratch/output
module swap compilers compilers/gnu
module swap mpi mpi/openmpi/1.10.1/gnu-4.9.2
module load python2/recommended
module load icommands
gerun /home/ccearal/.python2local/bin/newsrods query_20161101_1002.py /home/ccearal/Scratch/TDA/output/saved_ids.yml --fromfile --downsample 1 --outpath find_all_words_per_year_20161101_1002

