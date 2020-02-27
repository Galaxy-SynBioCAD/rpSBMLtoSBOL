FROM brsynth/rpbase:dev

RUN pip install pandas numpy scipy sklearn pysbol pySBOL synbiochem-py

COPY rpTool.py /home/
COPY rpToolServe.py /home/
COPY tool_rpSBMLtoSBOL.py /home/
