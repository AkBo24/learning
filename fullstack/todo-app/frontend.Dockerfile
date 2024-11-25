FROM node:23-alpine

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY ./package*.json ./
COPY ./webpack.config.js ./

# Install dependencies
RUN npm install

# # Copy the rest of the frontend application code
# COPY ./frontend .

# Expose the port for the React development server
EXPOSE 3000

# Start the development server
# CMD # ["npm", "run", "dev"]
