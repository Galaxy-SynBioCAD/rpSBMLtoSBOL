#!/usr/bin/env python3

import requests
import argparse
import json
import tarfile
import tempfile
import os
import glob

import sys
sys.path.insert(0, '/home/')
import rpToolServe

##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Given an rpSBML or a collection of rpSBML in a tar, convert to the SBOL format based on the selenzyme UNIPROT IDs')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-rbs', type=bool, default=True)
    parser.add_argument('-max_prot_per_react', type=int, default=3)
    parser.add_argument('-pathway_id', type=str, default='rp_pathway')
    params = parser.parse_args()
    if params.rbs=='True' or params.rbs=='true' or params.rbs==True or params.rbs=='T':
        rbs = True
    elif params.rbs=='False' or params.rbs=='false' or params.rbs==False or params.rbs=='F':
        rbs = False
    else:
        logging.error('Cannot parse the rbs input: '+str(params.rbs))
    #TODO: for the moment we will consider this parameter to be always None, need to change that
    tirs = None
    if params.input_format=='tar':
        rpToolServe.runRPSBMLtoSBOL_hdd(params.input,
                                        params.output,
                                        rbs,
                                        params.max_prot_per_react,
                                        tirs,
                                        params.pathway_id)
    elif params.input_format=='sbml':
        #make the tar.xz 
        with tempfile.TemporaryDirectory as tmpOutputFolder:
            input_tar = tmpOutputFolder+'/tmp_input.tar.xz'
            with tarfile.open(input_tar, mode='w:xz') as tf:
                info = tarfile.tarinfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                info.size = os.path.getsize(params.input)
                tf.addfile(tarinfo=info, fileobj=open(params.input, 'rb')) 
            rpToolServe.runRPSBMLtoSBOL_hdd(input_tar,
                                            params.output,
                                            rbs,
                                            params.max_prot_per_react,
                                            tirs,
                                            params.pathway_id)
    else:
        self.logging('cannot identify the input_format: '+str(params.input_format))
