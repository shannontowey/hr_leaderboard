FROM python:3

RUN pip install flask-restplus
RUN pip install flask-cors
RUN pip install webargs
RUN pip install datetime

COPY . /usr/local/hr_leaderboard/
WORKDIR /usr/local/hr_leaderboard/

ENTRYPOINT ["python"]
CMD ["hr_leaderboard.py", "hr_leaderboard.config"]
