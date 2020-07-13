# web-scraping-challenge
Using python to scrape websites for images, tables, and data

This project is the culmination of learning techniques to scrape websites for data. It runs on Python code, and utilizes HTML and CSS as well. 
The use of Flask was also required.

The website I created scrapes a few different websites for data on Mars:
- The NASA Mars news website for headline data,
- JPL's website for their featured image,
- The Mars weather Twitter page for the most current weather data from Mars,
- The Mars Fact webpage for a table of information about Mars, and
- The USGS Astrogeology website for images of each of Mars' hemispheres.

The most challenging part of this project was coming up with the method to scrape Twitter. Obviously, websites like Twitter make it difficult
to accurately scrape for data. To do so, I had to learn how to use Regular Expression Patterns along with the .find() method.

Next steps:
- Scrape more websites with data depending on a project. Ideas include tornado data from NOAA, or asteroid data from NASA.
