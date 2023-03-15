FROM python:3

#COPY test/httptest /var/www/html/test/httptest
#COPY . .
WORKDIR /app
COPY . /app


EXPOSE 5500

VOLUME [ "/app/etc" ]

CMD ["python3", "main.py"]