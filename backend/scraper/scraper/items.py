# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


# TODO: Convert location to locations
# TODO: Add a first posted date
class JobItem(Item):
    employer_name = Field()
    application_url = Field()
    job_title = Field()
    location = Field()
    job_department = Field()
    job_description = Field()
    employment_type = Field()
