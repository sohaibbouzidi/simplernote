FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production=false --no-audit --prefer-offline

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
