FROM public.ecr.aws/lambda/python:3.11

COPY sam.py FINDER_requirements.txt FINDER/setup.py ./

COPY ./FINDER ./FINDER

RUN python3.11 -m pip install -r FINDER_requirements.txt -t .
# RUN pip3 install gcc
ADD util.py ./game/util.py
# ADD FINDER/FINDER.cpython-312-darwin.so ./game/FINDER/FINDER.cpython-312-darwin.so
# ADD FINDER/FINDER.pyx ./game/FINDER/FINDER.pyx
# ADD FINDER/FINDER.cpython-312-x86_64-linux-gnu.so ./game/FINDER.cpython-312-x86_64-linux-gnu.so
# ADD FINDER/FINDER.c ./game/FINDER.c
RUN python setup.py build_ext --inplace

CMD ["sam.lambda_handler"]
