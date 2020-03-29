#!/usr/bin/env python
"""
03/26/2020 Tessa_main.py: This script serves as a wrapper of BriseisEncoder and Tessa, to generate TCR sequence embedding,
and/or to estimate functional landscape of TCR repertoire when combined with single-cell sequencing of T cells. Please
find more details in our paper: Mapping the Functional Landscape of TCR Repertoire. Zhang Z, Xiong D, et al.
"""
__author__='Ze Zhang'
__maintainer__='Ze Zhang'
__copyright__='Wang Lab, UT Southwestern Medical Center'
__version__='1.0.0'
__email__='ze.zhang@utsouthwestern.edu'

import sys
import os
from os.path import dirname
sys.path.append(dirname('./BriseisEncoder'))
sys.path.append(dirname('./Tessa'))
args = sys.argv

if '-tcr' in args:
    #Mode 1: Briseis encoder + Tessa
    # #Step 1: Run BriseisEncoder
    tcr_dir = args[args.index('-tcr')+1]
    model_dir=args[args.index('-model')+1]
    aa_dict_dir=args[args.index('-embedding_vectors')+1]
    output_encodedTCR_dir=args[args.index('-output_TCR')+1]
    output_log_dir = args[args.index('-output_log') + 1]
    if '-output_VJ' in args:
        output_encodedVJ_dir=args[args.index('-output_VJ')+1]
        cmd_encoder = ' '.join(['python3', './BriseisEncoder/BriseisEncoder.py', '-tcr', tcr_dir, '-model',
                                model_dir, '-embedding_vectors', aa_dict_dir,'-output_TCR',
                                output_encodedTCR_dir, '-output_VJ', output_encodedVJ_dir,
                                '-output_log', output_log_dir])
    else:
        cmd_encoder = ' '.join(['python3', './BriseisEncoder/BriseisEncoder.py', '-tcr', tcr_dir, '-model',
                                model_dir, '-embedding_vectors', aa_dict_dir, '-output_TCR',
                                output_encodedTCR_dir,'-output_log', output_log_dir])
    os.system(cmd_encoder)
    #Step 2: Run Tessa
    exp_file = args[args.index('-exp')+1]
    contigs_file = output_encodedTCR_dir
    cdr3_file = tcr_dir
    save_tessa = args[args.index('-output_tessa')+1]
    is_sampleCluster = args[args.index('-within_sample_networks')+1]
    if '-predefined_b' in args:
        fixed_b = args[args.index('-predefined_b')+1]
    else:
        fixed_b='NA'
    cmd_tessa1 = ' '.join(['Rscript', './Tessa/real_data.R', exp_file, contigs_file, cdr3_file,
                            save_tessa, is_sampleCluster, fixed_b])
    os.system(cmd_tessa1)
if '-embedding' in args:
    #Mode 2: Tessa only
    exp_file = args[args.index('-exp') + 1]
    contigs_file = args[args.index('-embedding') + 1]
    cdr3_file = args[args.index('-meta') + 1]
    save_tessa = args[args.index('-output_tessa') + 1]
    is_sampleCluster = args[args.index('-within_sample_networks') + 1]
    if '-predefined_b' in args:
        fixed_b = args[args.index('-predefined_b') + 1]
    else:
        fixed_b = 'NA'
    cmd_tessa2 = ' '.join(['Rscript', './Tessa/real_data.R', exp_file, contigs_file, cdr3_file,
                           save_tessa, is_sampleCluster, fixed_b])
    os.system(cmd_tessa2)
else:
    sys.exit('ERROR: please input valid TCRs/embedding.')