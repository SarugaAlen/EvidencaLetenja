# Use a lightweight Node.js image for building the application
FROM node:22-alpine AS builder

WORKDIR /app

# Kopiramo package.json in package-lock.json datoteke 
COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

# Odstranimo development dependencies
RUN npm prune --production


# Stage 2
# Use a lightweight Node.js image for running the application
FROM node:22-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app/build build/

# Copy the pruned node_modules directory (production dependencies only)
COPY --from=builder /app/node_modules node_modules/

# Copy the package.json file for metadata and application reference
COPY package.json .

# Expose the port on which the application will run
EXPOSE 3000

# Set the environment variable to production
ENV NODE_ENV=production

# Define the command to start the application
CMD [ "node", "build" ]
