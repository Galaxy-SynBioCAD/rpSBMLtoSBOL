#!/usr/bin/python

import tempfile
import tarfile
import glob
import logging

import rpTool


def runRPSBMLtoSBOL_hdd(inputTar, 
                        outputSBOL, 
                        rbs=True,
                        max_prot_per_react=3, 
                        tirs=None, 
                        pathway_id='rp_pathway'):
    with tempfile.TemporaryDirectory() as tmpInputFolder:
        tar = tarfile.open(inputTar, mode='r')
        tar.extractall(path=tmpInputFolder)
        tar.close()
        if len(glob.glob(tmpInputFolder+'/*'))==0:
            logging.error('Input file is empty')
            return False
        rpTool.convert(tmpInputFolder, outputSBOL, rbs, max_prot_per_react, tirs, pathway_id)
    return True
