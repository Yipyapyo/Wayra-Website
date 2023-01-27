# Venture Capital Portfolio Management Suite
## Team Kinkajou
The members of the team are:
- Lewis
- Saadh
- Kriyes
- Francis
- Adnan
- Kabir
- Chin
- Ken
- Fergan
- Reb

## Project structure
The project is called `vcpms` (Venture Capital Portfolio Management Suite).  It currently consists of a single app `portfolio` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *<[enter URL here](URL)>*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```


## Sources
The packages used by this application are specified in `requirements.txt`
