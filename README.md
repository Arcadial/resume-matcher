# Resume Matcher

This program matches uploaded resumes to jobs from LinkedIn through keyword matching and provides a compatibility percentage. Kubernetes deployed.

### To run
`python apply.py`\
(might take a while)

1. Allow the scraper to run completely
2. Navigate to http://localhost:80/
3. Upload a resume (only available in PDF and DOCX format)


### To stop

`python delete.py`


### Dependencies

1. Docker Desktop **with Kubernetes enabled**
2. MongoDB Compass (if you want to view the scraped jobs w/ their keywords)


### Additionals

For any changes to the scraper, edit scraper.py in ./scraper\
To find out more on the usage of the scraper: https://github.com/spinlud/py-linkedin-jobs-scraper

### Enabling kubernetes on Docker Desktop
Head to Docker Desktop settings and check both of them.

![image](https://github.com/Arcadial/resume-matcher/assets/81850188/a958ec4d-5c5c-4b4a-a548-6a31f6b105e5)

