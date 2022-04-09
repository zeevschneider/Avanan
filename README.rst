Table of Contents
=================

1. `General`_

2. `Specifications`_

3. `Installation and deployment`_

4. `Usage - tests`_

5. `Assumptions and Improvements`_


General
========
This program is a home assignment of Avanan.
It demonstrates testing related abilities:
1. Create testing planning doc : please see Q1.docx document
2. Creation of frontend tests using Selenium - please see test_walla_shops.py and walla.shops directory with support code
3. Testing of https://ipinfo.io/161.185.160.93/geo api with it's endpoints


Specifications:
===============
Each assignment has it's own specification described in the "Home assignment" document

Installation and deployment
===========================

1. Open a command line on your machine (verify git installation) and run the following:
    git clone git@github.com:zeevschneider/Avanan.git

2. Make sure that you have a machine with Python &gt;= 3.6 installed

3. Open a command line and cd to the /Avanan folder in the downloaded package

4. The best way is to install requirements into a virtual environment in order not to soil
    your python with unnecessary packages:
    a. Install virtualenv package - pip install virtualenv
    b. Create virtual environment:
        1. Make sure that you are in the /Avanan folder
        2. Run the following command – virtualenv {your_env_name}
        3. Activate your virtual environment – type {your_env_name}\Scripts\activate
        Your command line looks like the following:
        ({your_env_name}) {path}/Avanan
    c. Run the following command to install packages that are listed in the requirements.txt file:
       pip install -r requirements.txt
       You should receive a “Successfully installed…” message


Usage - tests:
======
Run tests:
    CD to /Avanan and type "pytest"




Assumptions and Improvements:
=============================

Wallashops tests - see more in the Q2.docx document:
=================
 1. Ran for guest user only
 2. Searches for a non specific product and handles the first one fount - i.e chair

Api tests:
=========
 Showing only basics.
 TODO: Writing additional tests for every endpoint - positive and negative testing
