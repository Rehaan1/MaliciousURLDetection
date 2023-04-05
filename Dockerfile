FROM node:18-alpine

RUN apk update && apk add python3
RUN apk add py3-pip && pip3 install pandas joblib && pip3 install -U scikit-learn==0.21.3

ENV PORT=3000
WORKDIR /app
EXPOSE 3000

COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

COPY . .
CMD [ "node", "app.js" ]
