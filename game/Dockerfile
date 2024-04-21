FROM public.ecr.aws/lambda/python:3.12

COPY sam.py FINDER_requirements.txt ./FINDER/ ./

RUN python3.12 -m pip install -r FINDER_requirements.txt -t .
ADD util.py ./game/util.py
# RUN python setup.py build_ext --inplace
CMD ["sam.lambda_handler"]
