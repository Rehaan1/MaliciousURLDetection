FROM node:18-alpine
RUN apt-get update || : && apt-get install python -y

ENV PORT=3000
WORKDIR /app
EXPOSE 3000

COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

COPY . .
CMD [ "node", "app.js" ]