FROM public.ecr.aws/lambda/python:3.11
COPY sam.py FINDER_requirements.txt ./FINDER/ ./

RUN python3.11 -m pip install -r FINDER_requirements.txt -t .
RUN yum install -y gcc-c++

ADD util.py ./game/util.py
RUN python setup.py build_ext --inplace
CMD ["sam.lambda_handler"]
