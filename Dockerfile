FROM python
COPY . /usr/src
WORKDIR /usr/src
# RUN apt-get update && apt-get install -y fish mc
RUN python -m pip install -r ./requirements.txt
RUN python ./build.py reden
CMD ./dist/reden/reden.exe