FROM python:3.11-slim-buster
EXPOSE 5000

# Set working directory
WORKDIR /app


RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev

# Install prerequisites
RUN apt-get install -y apt-transport-https
RUN apt-get install -y sudo
# Import Microsoft GPG key
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

# Add Microsoft repository
RUN curl https://packages.microsoft.com/config/debian/10/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# Update package list
RUN apt-get update

# Install Microsoft ODBC driver
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Install mssql-tools (optional)
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools

# Add mssql-tools to PATH
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile

# Install unixODBC development headers (optional)
RUN apt-get install -y unixodbc-dev

# Install kerberos library for debian-slim distributions (optional)
RUN apt-get install -y libgssapi-krb5-2


# Copy application code
COPY . .

RUN pip install -r requirements.txt

# Run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]
