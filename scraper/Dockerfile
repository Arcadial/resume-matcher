FROM spinlud/python3-selenium-chrome

WORKDIR /scraper

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm

COPY . .

CMD python scraper.py && python job_description_identifier.py