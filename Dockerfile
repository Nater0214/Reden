FROM python
COPY . /usr/src
WORKDIR /usr/src
RUN apt-get update && apt-get install -y net-tools
RUN python -m pip install -r requirements.txt
# RUN python ./build.py reden
# CMD ./dist/reden/reden
CMD python main.py