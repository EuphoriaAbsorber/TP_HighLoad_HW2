# TP_HighLoad_HW2

# Thread pool Python


# Server requirements:

* Respond to `GET` with status code in `{200,404,403}`
* Respond to `HEAD` with status code in `{200,404,403}`
* Respond to all other request methods with status code `405`
* Directory index file name `index.html`
* Respond to requests for `/<file>.html` with the contents of `DOCUMENT_ROOT/<file>.html`
* Requests for `/<directory>/` should be interpreted as requests for `DOCUMENT_ROOT/<directory>/index.html`
* Respond with the following header fields for all requests:
  * `Server`
  * `Date`
  * `Connection`
* Respond with the following additional header fields for all `200` responses to `GET` and `HEAD` requests:
  * `Content-Length`
  * `Content-Type`
* Respond with correct `Content-Type` for `.html, .css, js, jpg, .jpeg, .png, .gif, .swf`
* Respond to percent-encoding URLs
* Correctly serve a 2GB+ files
* No security vulnerabilities

---------------------------
# Build docker containers

**Web server**
```
docker build -t server -f Dockerfile .
docker run -d --network host --name test1 server
```

**Nginx**
```
docker build -t nginx -f nginx.Dockerfile .
docker run -p 9090:9090 nginx
```

--------------------------
# Functional testing
```
python3 httptest.py
```
![изображение](https://user-images.githubusercontent.com/65418582/225330803-94bb10c0-1d55-401c-bacf-0ca317d11363.png)

--------------------------
# Load testing
Using [Apache Benchmark](https://httpd.apache.org/docs/2.4/programs/ab.html)
# Web server
```
ab -n 50000 -c 200 127.0.0.1:8080/httptest/wikipedia_russia.html
```
# 8 threads
![изображение](https://user-images.githubusercontent.com/65418582/225332608-a2b91816-05f0-4385-92ec-ec4dde177218.png)

# 32 threads
![изображение](https://user-images.githubusercontent.com/65418582/225332707-dd3aca06-e222-4865-9c96-55d44255f213.png)

# nginx
```
ab -n 50000 -c 200 127.0.0.1:9090/httptest/wikipedia_russia.html
```
![изображение](https://user-images.githubusercontent.com/65418582/225332835-7e16e095-32f1-44f2-89d9-ec6d5f9f69b1.png)

Сравнение RPS

| server \ workers              | 4       | 32      | 64      |
| --------------------------    |  :---:  | :-----: | :-----: |
| server                        | 1135.02 | 1261.29 | 1598.87 |
| nginx                         | 1149.82 | 1116.46 | 1180.10 |
