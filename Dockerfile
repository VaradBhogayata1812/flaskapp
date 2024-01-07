FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
COPY *.py /home/
COPY templates/*.* /home/templates/
ENV API_KEY '899e7f953bbd925e4e246d3a54c3e65f'
ENTRYPOINT ["python"]
CMD ["/home/catalogue.py" ]
EXPOSE 5000
