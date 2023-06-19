# Base image
FROM node:16.20.0-alpine3.18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project
COPY . .

# Build the React app
RUN npm run build

# Start the app
CMD ["npm", "start"]
