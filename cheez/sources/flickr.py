from cheez.types import ImageInfo, Namespace
import json
import random
import requests
import time

import flickrapi


class SECONDS_IN:
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR


def _client(keys_filename: str, *args, **kwargs):
    with open(keys_filename) as f:
        keys = json.load(f)

    flickr = flickrapi.FlickrAPI(keys['key'], keys['secret'], *args, **kwargs)
    return flickr


def _process_search_date(date: str):
    date = date.strip()
    if date.startswith('-'):
        date = date.lstrip('-')
        if ' ' in date:
            days, seconds = date.rsplit(None, 1)
        else:
            days, seconds = '0', date
        time_back = 0
        time_amount = 1
        for part in reversed(seconds.split(':')):
            time_back += float(part) * time_amount
            time_amount *= 60
        time_back += float(days) * SECONDS_IN.DAY
        date = str(time.time() - time_back)
    return date


def _process_search_terms(**terms):
    for name, value in sorted(terms.items()):
        if value:
            if name.endswith('date'):
                value = _process_search_date(value)
            yield name, value


def search_photos(flickr, args: Namespace):
    flickr = flickr or _client(args.keys, format='parsed-json')

    search_terms = dict(_process_search_terms(
        content_type='1',  # Photos only
        group_id=args.group_id,
        is_commons=args.is_commons,
        license=','.join(args.license) if args.license else '7,8',  # Default to PD images
        media='photos',  # Photos, not videos
        max_taken_date=args.max_taken_date,
        max_upload_date=args.max_upload_date,
        min_taken_date=args.min_taken_date,
        min_upload_date=args.min_upload_date,
        per_page=args.limit,
        safe_search=args.safe_search,
        tags=','.join(args.tags or ()),
        tag_mode=args.tag_mode,
        text=args.text,
        user_id=args.user_id,
    ))

    photos = flickr.photos.search(**search_terms)
    return [(photo['id'], photo['title']) for photo in photos['photos']['photo']]


def get_photo_source(flickr, photo_id, width=None, height=None):
    sizes = flickr.photos.getSizes(photo_id=photo_id)
    size_urls = sorted([
        (int(size['width']), int(size['height']), size['source'])
        for size in sizes['sizes']['size']
    ])
    for swidth, sheight, source in size_urls:
        if swidth >= width > 0 or sheight >= height > 0:
            return source
    else:
        return source  # Last one is largest


def get_photo_info(flickr, photo_id):
    info = flickr.photos.getInfo(photo_id=photo_id)
    title = info['photo']['title']['_content']
    description = info['photo']['description']['_content']
    return title, description


def from_flickr(args: Namespace)-> ImageInfo:
    flickr = _client(args.keys, format='parsed-json')

    photos = search_photos(flickr, args)

    photo_id, title = random.choice(photos)
    title, description = get_photo_info(flickr, photo_id)
    url = get_photo_source(flickr, photo_id, width=args.width, height=args.height)
    response = requests.get(url)
    image = ImageInfo(url=url, bytes=response.content, title=title, description=description)

    return image


