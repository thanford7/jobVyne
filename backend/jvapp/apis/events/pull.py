import abc
import datetime
import json
import logging
from abc import ABC
from collections import deque

from jvapp.apis.geocoding import LocationParser
from jvapp.models.content import Event
from jvapp.models.employer import Employer
from scrape.reader import WebReader

logger = logging.getLogger(__name__)

def pull_events(limit):
    num_events_pulled = 0

    web_reader = WebReader()
    events = []
    try:
        for event_source_class in event_source_classes:
            event_source = event_source_class(web_reader, events)
            while event_source.has_more() and num_events_pulled < limit:
                event_source.get_next()
                num_events_pulled += 1
    finally:
        web_reader.complete()

    # Use `save` so that audit times are set
    for event in events:
        event.save()


class EventSource(abc.ABC):
    def __init__(self, web_reader, events):
        self.web_reader = web_reader
        self.events = events

    @abc.abstractmethod
    def has_more(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_next(self):
        """"Return the next Event model object pulled from the source"""
        raise NotImplementedError


class EventListSource(EventSource, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_src_queue = None  # Initialize as deque of objects that each represent one event (e.g. BS markup objects or parsed JSON)

    @abc.abstractmethod
    def parse_event_src(self, event_bs):
        raise NotImplementedError

    def has_more(self):
        return len(self.event_src_queue) > 0

    def get_next(self):
        if event := self.parse_event_src(self.event_src_queue.popleft()):
            self.events.append(event)


class MeetupSource(EventListSource):
    name = None
    slug = None
    group = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        index_page_bs = self.web_reader.read_sync(f'https://www.meetup.com/{self.slug}/events/')
        next_data_dict = json.loads(index_page_bs.select('#__NEXT_DATA__')[0].text)
        apollo_state_dict = next_data_dict['props']['pageProps']['__APOLLO_STATE__']
        self.venues_by_id = {
            v['id']: v for k, v in apollo_state_dict.items()
            if k.startswith('Venue')
        }
        self.event_src_queue = deque(
            v for k, v in apollo_state_dict.items()
            if k.startswith('Event')
        )

    def parse_event_src(self, event_dict):
        event_url = event_dict['eventUrl']
        if Event.objects.filter(source_url=event_url).exists():
            logger.info(f'Event for URL {event_url} has already been pulled; skipping.')
            return None

        venue_dict = event_dict['venue']
        location = None
        if venue_dict:
            venue_id = venue_dict['__ref'].split(':')[1]
            venue_dict = self.venues_by_id[venue_id]
            location_text = ', '.join(venue_dict.get(k) for k in ('address', 'city', 'state', 'country'))
            location = LocationParser().get_location(location_text)
        event = Event(
            source=self.name,
            source_url=event_url,
            name=event_dict['title'],
            location=location,
            description=event_dict['description'],
            start_dt=datetime.datetime.fromisoformat(event_dict['dateTime']),
            end_dt=datetime.datetime.fromisoformat(event_dict['endTime']),
            group=self.group,
        )
        return event


class CPM(MeetupSource):
    name = 'Colorado Product Meetup'
    slug = 'colorado-product'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = Employer.objects.get(employer_name='Hospital IQ')

event_source_classes = [CPM]