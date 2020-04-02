FROM brsynth/rpbase:dev

RUN pip install pandas numpy scipy sklearn pysbol pySBOL synbiochem-py

#RUN wget https://raw.githubusercontent.com/neilswainston/SbmlToSbol/master/sbml2sbol/converter.py
#RUN mv converter.py rpTool.py

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY tool_rpSBMLtoSBOL.py /home/
