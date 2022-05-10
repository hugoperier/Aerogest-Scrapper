<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/hugoperier/Aerogest-Scrapper">
    <img src="http://www.aerogest-reservation.com/Content/images/aerogest_resa.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Aerogest Scrapper</h3>

  <p align="center">
    A web scrapper made for aerogest.com.
    <br />
    <a href="https://github.com/hugoperier/Aerogest-Scrapper/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/hugoperier/Aerogest-Scrapper/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/hugoperier/Aerogest-Scrapper/Best-README-Template/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The process of finding schedule in aerogest.com is time consuming and tedious. You need to login, search for an available pilot instructor as well as a schedule for the plane you are flying with. There is no notification system available in the website to notify you when the schedule is available. I belive this project is the solution to the problem.

Here's why:
* Your time should be focused on learning how to pilot and not on finding a schedule.
* Sometime it is hard to find a schedule for a precise instructor (particulary on the weekend).
* You save enought time to star this repo 😃

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [python 3.9](https://www.python.org)
* [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [cssutils](https://pypi.org/project/cssutils/)
* [python-requests](https://docs.python-requests.org/en/latest/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

This project have been build with python and the dependancies are managed with pipenv.
Those are mandatory to run the project.
* python 3.9
  ```sh
  sudo apt install python3.8
  ```
* pipenv
  ```sh
  pip3 install pipenv
    ```

### Installation


1. Clone the repo
   ```sh
   git clone https://github.com/hugoperier/Aerogest-Scrapper
   ```
3. Install pip packages
   ```sh
   pipenv install
   ```
4. rename the default configuration file
   ```sh
   mv default.template.conf default.conf
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

There is a configuration file named default.conf in the root directory of the project.
This file is used to configure the scrapper. It contains informations about the aeroclub you targets, credentials that will be used to log in and fetch informations, and some configuration for the scrapper.

### Example

```py
[AEROGEST_INFOS]
HOST=http://www.aerogest-reservation.com
CLUB_ID=aeroclub_bellegarde

[CREDENTIALS]
LOGIN=9874 
PASSWORD=31021978

[SCHEDULESFINDER]
# The scrapper will look for schedules for the following days
WEEKDAYS=lundi,mardi,mercredi,jeudi,vendredi,samedi,dimanche
# The duration is expressed in minutes
DURATION=120
# Trigram must be used for the instructor selection
INSTRUCTORS=KAT
# Airplane registration must be use for the airplane selection 
AIRPLANE=F-GTFC
# The number of days to look into, starting from the current day
SEARCHRANGE=40
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Create schedule finder
- [ ] Create tests
- [ ] Notification module
    - [ ] Email
    - [ ] Sendgrid

See the [open issues](https://github.com/hugoperier/Aerogest-Scrapper/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Hugo PERIER - [website](https://hugoperier.eu) - hugo.perier@protonmail.com

Project Link: [https://github.com/hugoperier/Aerogest-Scrapper](https://github.com/hugoperier/Aerogest-Scrapper)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/hugo-perier-forreal/