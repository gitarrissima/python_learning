1. как запускать
python3 httpd.py

2. архитектура: асинхронность реализована с помощью threading
каждый новый запрос обрабатывается в отдельном треде

3. результаты нагрузочного тестирования:

root@ubuntu1804:~/python_learning# ab -n 50000 -c 100 -r http://localhost:80/
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        ubuntu1804
Server Hostname:        localhost
Server Port:            80

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   388.255 seconds
Complete requests:      50000
Failed requests:        0
Non-2xx responses:      50000
Total transferred:      2300000 bytes
HTML transferred:       0 bytes
Requests per second:    128.78 [#/sec] (mean)
Time per request:       776.511 [ms] (mean)
Time per request:       7.765 [ms] (mean, across all concurrent requests)
Transfer rate:          5.79 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   6.6      0    1032
Processing:     6  776  53.1    773    1474
Waiting:        6  775  53.1    772    1474
Total:         13  776  53.4    773    1780

Percentage of the requests served within a certain time (ms)
  50%    773
  66%    788
  75%    796
  80%    800
  90%    816
  95%    828
  98%    868
  99%    940
 100%   1780 (longest request)
