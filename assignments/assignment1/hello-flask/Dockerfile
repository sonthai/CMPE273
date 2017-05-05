FROM python:2.7.13
MAINTAINER Son Thai "son.thai@sjsu.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

