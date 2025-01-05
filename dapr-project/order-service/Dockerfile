# Use the official Node.js LTS image as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY app.js .

# Expose the port that the application will run on
EXPOSE 5002

# Start the application
CMD ["node", "app.js"]
