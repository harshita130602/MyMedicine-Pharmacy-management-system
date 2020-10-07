# MyMedicine - PyMySQL Project (Phase 4)

This repository is an attempt to create a mini world of “MyMedicine - An Online Pharmacy Management System”.  It is a system that stores data and enables functionality that allows users to buy medicines via an online network.  To be precise, pharmacy management system is an internet-based vendor that sells medicines and allowsusers an option to buy from their mobile, laptop etc. 

The CLI version for the same can be run by cloning this repo.

### Requirements

* Python3
```sh
$ sudo apt-get update
$ sudo apt-get install python3.6
```
* MySQL
* PyMySQL
```sh
$ sudo apt-get install python3-pip
$ pip3 install pymysql
```

### Installation

You will need to replicate the MyMedicine Databse on your local machine, for which the dump.sql file is provided herewith.

Open your MySQL server and create the following database:

```sh
$ mysql> CREATE DATABASE MYMEDICINE;
```

Run the following command to import the database:

```sh
$ mysql -u username -p MYMEDICINE < dump.sql
```

You might need to enter your password in the next step.

To run the CLI, change your directory to the cloned folder and run the following command:

```sh
$ python3 MyMedicine.py
```

``` diff
- Please Note: If you are using Docker to run MySQL, you might need to first change your port to 5005 (or the port you use) by replacing the following lines for connecting the database in the MyMedicine.py file: 
```

```sh
con = pymysql.connect(host='localhost',
                              user=username,
                              password=password,
                              db='MYMEDICINE',
                              port='5005',
                              cursorclass=pymysql.cursors.DictCursor)
```

near lines 1086-1090.

### Steps to Run

You will be first prompted to enter your MySQL Username and Password as follows:

```sh
Enter username and password to access the database.
Username: 
Password:
```

You will now be redirected to the Login/Signup Page.

The following are some sample credentials for you to login (although you can create yours too from the CLI):

* Admin
```sh
Email-Id: prajneya@admin.com 
Password: 1234
```
* Customer
```sh
Email-Id: prajneya@customer.com 
Password: 1234
```
* Manager
```sh
Email-Id: prajneya1@manager.com 
Password: 1234
```
```sh
Email-Id: prajneya2@manager.com 
Password: 1234
```
```sh
Email-Id: prajneya3@manager.com 
Password: 1234
```
*Happy Shopping! :heart: *
