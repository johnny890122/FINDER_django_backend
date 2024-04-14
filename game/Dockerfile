FROM public.ecr.aws/lambda/python:3.12

COPY sam.py FINDER_requirements.txt ./

RUN python3.12 -m pip install -r FINDER_requirements.txt -t .
ADD util.py ./game/util.py

CMD ["sam.lambda_handler"]
