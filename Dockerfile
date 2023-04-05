FROM node:18
RUN apt-get update || : && apt-get install -y python3.6=3.6.9-1~18.04ubuntu1.4

RUN apt install python3-pip -y
RUN pip3 install pandas
RUN pip3 install joblib
RUN pip3 install -U scikit-learn==0.21.3

ENV PORT=3000
WORKDIR /app
EXPOSE 3000

COPY ["package.json", "package-lock.json*", "./"]
RUN npm install

COPY . .
CMD [ "node", "app.js" ]