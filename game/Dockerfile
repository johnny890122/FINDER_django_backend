# FROM public.ecr.aws/lambda/python:3.11-x86_64
# COPY FINDER_requirements.txt ./FINDER/ ./

# RUN python3.11 -m pip install -r FINDER_requirements.txt -t .
# RUN yum -y install gcc-c++

# ADD util.py ./game/util.py
# RUN python setup.py build_ext --inplace

FROM my_image:latest
COPY sam.py ./
CMD ["sam.lambda_handler"]
