FROM node:18

# Install required system packages
RUN apt-get update || : && apt-get install -y python3 python3-pip

# Install Python packages
RUN pip3 install pandas joblib scikit-learn==0.24.2

# Set environment variables
ENV PORT=3000

# Set working directory and expose port
WORKDIR /app
EXPOSE 3000

# Install Node.js packages
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

# Copy application files
COPY . .

# Start the application
CMD [ "node", "app.js" ]
