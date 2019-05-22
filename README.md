# PresentEasyModernized
Good Ol' Present Easy with a Better Backend Infrastructure 

### Deployed here: http://18.222.96.13/ (Docs Comming Soon!)

# Tech Stack
## 1. **Flask Web App**
 - Flask backed backend!
 - JWT Token Based Authentication
## 2. **Redis Caching Layer**
 - Caches images on a redis server for quick retervial
 - Cache is invalidated every hour
## 3. **Postgres DB**
 - Persisted storage containg 2 models (Users & Images)
## 4. **Dockerized Repo**
 - Postgres, Redis and App images are defined in the docker-compose file
## 5. **AWS**
 - Dockerized Application hosted on a t2.micro EC2 Instance
