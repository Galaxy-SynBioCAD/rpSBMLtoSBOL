#!/usr/bin/python

import tempfile
import tarfile
import glob
import logging
import os

import rpTool
import rpSBML


def runRPSBMLtoSBOL_hdd(inputTar, 
                        outputSBOL, 
                        rbs=True,
                        max_prot_per_react=3, 
                        tirs=None, 
                        topX=5,
                        pathway_id='rp_pathway'):
    """Convert a collection of rpSBML into a collection of SBOL

    :param inputTar: The path to the TAR collection of rpSBML
    :param outputSBOL: The path to the output TAR collection of SBOL
    :param rbs: Calculate or not the RBS strength
    :param max_prot_per_react: The maximum number of proteins per reaction (Default: 3)
    :param tirs: The RBS strength values
    :param topX: The top number of UNIPROT id's per reaction to use
    :param pathway_id: The Groups id of the heterologous pathway

    :type inputTar: str
    :type outputSBOL: str
    :type rbs: bool
    :type max_prot_per_react: int
    :type tirs: list
    :type topX: int
    :type pathway_id: str

    :rtype: bool
    :return: The success or failure of the function
    """
    logging.info(rbs)
    with tempfile.TemporaryDirectory() as tmpInputFolder:
        tar = tarfile.open(inputTar, mode='r')
        tar.extractall(path=tmpInputFolder)
        tar.close()
        #return only the topX global score pathways
        if len(glob.glob(tmpInputFolder+'/*'))==0:
            logging.error('Input file is empty')
            return False
        file_names_score = {}
        for sbml_path in glob.glob(tmpInputFolder+'/*'):
            file_name = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '').replace('.rpsbml', '')
            rpsbml = rpSBML.rpSBML(file_name)
            rpsbml.readSBML(sbml_path)
            groups = rpsbml.model.getPlugin('groups')
            rp_pathway = groups.getGroup(pathway_id)
            if not rp_pathway:
                logging.error('Cannot retreive the pathway: '+str(pathway_id))
                return False
            brsynth_annot = rpsbml.readBRSYNTHAnnotation(rp_pathway.getAnnotation())
            try:
                file_names_score[sbml_path] = brsynth_annot['global_score']['value']
            except KeyError:
                logging.warning('Cannot retreive the global_score from: '+str(file_name)+'('+str(brsynth_annot)+')')
                pass
        logging.info(file_names_score)
        top_file_names = [k for k, v in sorted(file_names_score.items(), key=lambda item: item[1], reverse=True)][:topX]
        logging.info(top_file_names)
        for todel in [i for i in glob.glob(tmpInputFolder+'/*') if i not in top_file_names]:
            os.remove(todel)
        #### convert to SBOL ####
        rpTool.convert(tmpInputFolder, outputSBOL, rbs, max_prot_per_react, tirs, pathway_id)
    return True
