FROM python:3.9

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client graphviz \
    && rm -rf /var/lib/apt/lists/* && adduser --disabled-password python
RUN addgroup --gid 1006 developers \
    && usermod -a -G developers python
USER python
RUN mkdir ~/app && mkdir ~/.vscode-server
WORKDIR /home/python/app
COPY ./assets/requirements.txt ./
COPY ./src/co2calculator/requirements.txt ./requirements_co2calculator.txt
ENV PATH="/home/python/.local/bin:${PATH}"
RUN pip install -r requirements.txt
RUN pip install -r requirements_co2calculator.txt
EXPOSE 8000
WORKDIR /home/python/app/src
ENTRYPOINT [ "./entryPoint.sh" ]
