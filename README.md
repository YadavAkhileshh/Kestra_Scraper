# Web Scraper with Kestra
A web scraping pipeline using Python and Kestra for orchestration.


#Features

-Automated Scheduling: Scrape data at regular intervals without manual intervention.

-Configurable URLs: Easily customize the target websites for scraping.

-Kestra Integration: Ensures robust orchestration and monitoring of the scraping pipeline.

-Efficient Data Extraction: Optimized for speed and reliability.

-Scalable Design: Easily add more scraping tasks as needed.


#Prerequisites
-Ensure you have the following installed:

-Python 3.8+

-Kestra Orchestrator


#Example configuration:
-scraping:

  urls:
    - https://quotes.toscrape.com/
    - https://quotes.toscrape.com/page/2/
  schedule: "0 12 * * *" # Every day at noon
  
-output:

  type: csv
  path: ./output/

Monitor the pipeline using Kestra’s dashboard to view logs, schedules, and execution results.


#Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch (git checkout -b feature-name).

Commit your changes (git commit -m 'Add feature').

Push to the branch (git push origin feature-name).

Create a Pull Request.



Thanks to the Kestra team for their amazing orchestration platform.

Inspired by the need for efficient and automated data extraction pipelines.

Contact
For any inquiries, please reach out to yadavakhil2501@gmail.com.

