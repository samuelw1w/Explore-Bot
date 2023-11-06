# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /workspaces/explorebot/myproject

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt /tmp/

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Make port 80 available to the world outside this container (if you have any web services)
#EXPOSE 80

# Define environment variable (if needed)
# ENV NAME World

# Run your script when the container launches (Change this as per your entry script)
#CMD scrapy crawl myspider && \
#python3 /explorebot/explorebot/myproject/scraper.py &&
