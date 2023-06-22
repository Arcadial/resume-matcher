# Resume Matcher

This program matches uploaded resumes to jobs from LinkedIn through keyword matching and provides a compatibility percentage. Fully dockerized with docker-compose and deployed to kubernetes.

### To run in kubernetes, change to k8s branch.

### To run
`docker-compose up --build`\
(might take a while)

1. Allow the scraper to run completely
2. Navigate to http://localhost:3000/
3. Upload a resume (only available in PDF and DOCX format)


### To stop

Ctrl+C\
`docker-compose down`


### Dependencies

1. Docker Desktop
2. MongoDB Compass (if you want to view the scraped jobs w/ their keywords)


### Additionals

For any changes to the scraper, edit scraper.py in ./scraper\
To find out more on the usage of the scraper: https://github.com/spinlud/py-linkedin-jobs-scraper

