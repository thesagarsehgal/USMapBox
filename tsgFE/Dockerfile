FROM node:18-alpine

WORKDIR /app

EXPOSE 3000

COPY package.json ./

# RUN npm config set rollup_platform linux-x64

RUN npm install --silent

COPY . ./

CMD ["npm", "run", "dev"]
# CMD ["sh", "-c", "npm install && npm run dev"]
