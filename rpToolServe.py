#!/usr/bin/python

import tempfile
import tarfile
import glob

import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api

import rpTool


def runRPSBMLtoSBOL_hdd(inputTar, 
                        outputSBOL, 
                        rbs=True,
                        max_prot_per_react=3, 
                        tirs=None, 
                        pathway_id='rp_pathway'):
    with tempfile.TemporaryDirectory() as tmpInputFolder:
        tar = tarfile.open(fileobj=inputTar, mode='r')
        tar.extractall(path=tmpInputFolder)
        tar.close()
        rpTool.convert(tmpInputFolder, outputSBOL, rbs, max_prot_per_react, tirs, pathway_id)
    return True
        
#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


def stamp(data, status=1):
    appinfo = {'app': 'rpSBMLtoSBOL', 'version': '0.1',
               'author': 'Neil Swanston, Melchior du Lac',
               'organization': 'Manchester University, BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """ REST App."""
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


class RestQuery(Resource):
    """ REST interface that generates the Design.
        Avoid returning numpy or pandas object in
        order to keep the client lighter.
    """
    def post(self):
        inputTar = request.files['inputTar']
        params = json.load(request.files['data'])
        #pass the files to the rpReader
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            #### HDD ####
            runRPSBMLtoSBOL_hdd(inputTar,
                                tmpOutputFolder+'/sbol.xml',
                                params['rbs'],
                                params['max_prot_per_react'], 
                                params['tirs'], 
                                params['pathway_id'])
            return send_file(open(tmpOutputFolder+'/sbol.xml', 'rb'), as_attachment=True, attachment_filename='sbol.xml', mimetype='application/xml')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
