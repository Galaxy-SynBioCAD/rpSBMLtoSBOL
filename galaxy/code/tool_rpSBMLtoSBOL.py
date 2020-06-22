#!/usr/bin/env python3

import requests
import argparse
import json
import tarfile
import tempfile
import os
import glob
import logging

import sys
sys.path.insert(0, '/home/')
import rpToolServe

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Given an rpSBML or a collection of rpSBML in a tar, convert to the SBOL format based on the selenzyme UNIPROT IDs')
    parser.add_argument('-input', type=str, help='input file path', required=True)
    parser.add_argument('-input_format', type=str, help='input file format. May be either "tar" (i.e. collection of SBML in tar archive) or "sbml"', required=True)
    parser.add_argument('-output', type=str, help='output SBOL file path', required=True)
    parser.add_argument('-rbs', type=str, default='True', help='calculate the RBS?')
    parser.add_argument('-topX', type=int, default=5, help='convert the top X scoring SBML files')
    parser.add_argument('-tirs', type=str, default='10000,20000,30000', help='RBS numbers relative strengths (must be the same length of "max_prot_per_react")')
    parser.add_argument('-max_prot_per_react', type=int, default=3, help='number of RBS per reactions')
    parser.add_argument('-pathway_id', type=str, default='rp_pathway', help='name of the heterologous pathway in the SBML files')
    params = parser.parse_args()
    if params.rbs=='True' or params.rbs=='true' or params.rbs==True or params.rbs=='T':
        rbs = True
    elif params.rbs=='False' or params.rbs=='false' or params.rbs==False or params.rbs=='F':
        rbs = False
    else:
        logging.error('Cannot parse the rbs input: '+str(params.rbs))
        exit(1)
    try:
        tirs = [int(i) for i in params.tirs.split(',')]
    except ValueError:
        logging.error('Invalid tirs input: '+str(params.tirs))
        exit(1)
    #TODO: add check that the -tirs length is the same as -max_prot_per_react
    if params.input_format=='tar':
        rpToolServe.runRPSBMLtoSBOL_hdd(params.input,
                                        params.output,
                                        rbs,
                                        params.max_prot_per_react,
                                        tirs,
                                        params.topX,
                                        params.pathway_id)
    elif params.input_format=='sbml':
        #make the tar.xz 
        with tempfile.TemporaryDirectory as tmpOutputFolder:
            input_tar = tmpOutputFolder+'/tmp_input.tar'
            with tarfile.open(input_tar, mode='w:gz') as tf:
                info = tarfile.tarinfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                info.size = os.path.getsize(params.input)
                tf.addfile(tarinfo=info, fileobj=open(params.input, 'rb')) 
            rpToolServe.runRPSBMLtoSBOL_hdd(input_tar,
                                            params.output,
                                            rbs,
                                            params.max_prot_per_react,
                                            tirs,
                                            params.topX,
                                            params.pathway_id)
    else:
        self.logging('cannot identify the input_format: '+str(params.input_format))
        exit(1)
