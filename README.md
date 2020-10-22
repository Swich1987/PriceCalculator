# PriceCalculator
Price calculator to calculate discount and state tax.

## Requirements
- docker 1.10.0+ with docker-compose

## Launch
Run in project folder:
```
docker-compose up -d
```

By default service will be launched on port 8000 of localhost. You can change it in `docker-compose.yml`, for example
 to run service on port 9500, change ports settings to `9500:8000`.
 
Depends on how you installed docker, you may need to use `sudo` command here and later:
```
sudo docker-compose up -d
```
 
## Stop
```
docker-compose down
```

## After launch

Open in any browser localhost:8000

## Change taxes or discounts
You can change settings in http://localhost:8000/admin page, but before you need to create superuser. 
To do this just complete this command after launch:
```
docker exec -it pricecalculator_web_1 python manage.py createsuperuser
```
and enter your login, e-mail and password.

`pricecalculator_web_1` is container name, which can differ on you local machine and is printed after launch, or you
 can use `docker ps` to see it's name.