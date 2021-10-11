# Use the Python 3.6.15 container image
FROM python:3.6.15-bullseye

# Set the working directory to /flask-app
WORKDIR /flask-app

# Copy the current directory contents into /flask-app
COPY . /flask-app

# Create and Activate virtual envirnmont
ENV VIRTUAL_ENV=/flask-app/flaskenv
RUN python3.6 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies and Copy custom python modules to venv site-packages
RUN pip install --no-cache-dir -r requirements.txt \
    && cp -r $(find -name "mymodules")  $(find -name "site-packages")

# Expose port 5000
EXPOSE 5000

# Run the FlaskApp application
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
