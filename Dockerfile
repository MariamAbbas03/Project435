# start by pulling the python image
FROM python:3.8-alpine
# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
# switch working directory
WORKDIR /app
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# copy every content from the local file to the image
COPY . /app

# uncomment the command with the application we need to create an image for
#CMD ["python3", "service1.py"]
#CMD ["python3", "service2.py"]
#CMD ["python3", "service3.py"]