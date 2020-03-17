FROM brsynth/rpbase

RUN pip install pandas numpy scipy sklearn pysbol pySBOL synbiochem-py

COPY rpTool.py /home/
COPY rpToolServe.py /home/
