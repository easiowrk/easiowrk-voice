# frontend/Dockerfile
FROM node:18

WORKDIR /app

# Copy package.json first (better cache)
COPY package*.json ./

# Install dependencies
RUN npm install

# Fix lightningcss binary for Linux container
RUN npm rebuild lightningcss --force

# Copy the rest of the frontend code
COPY . .

# Build Next.js app
RUN npm run build

EXPOSE 3000

# Run in dev mode (you can switch to start for prod)
CMD ["npm", "run", "dev"]
