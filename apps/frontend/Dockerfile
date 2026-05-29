FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --production=false --no-audit

COPY . .

EXPOSE 3000
CMD ["sh", "-c", "npm run build && npx nuxi preview --port 3000"]
