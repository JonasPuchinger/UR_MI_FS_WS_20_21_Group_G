import datetime

def date_range(start, end, step=13, date_format="%Y-%m-%d"):
    """
    Creates a list with a range of dates.
    The dates occur every 13th day (default).
    
    :param start: the start date of the date range
    :param end: the end date of the date range
    :param step: the step size of the dates
    :param date_format: the string format of the dates inputted and returned
    """
    start_date = datetime.datetime.strptime(str(start), date_format)
    end_date = datetime.datetime.strptime(str(end), date_format)
    num_days = (end_date - start_date).days
    
    for d in range(0, num_days + step, step):
        date_i = start + datetime.timedelta(days=d)
        yield date_i.strftime(date_format)
        
def twitter_requests(screen_names, start, end, step=13, date_format="%Y-%m-%d"):
    """
    Creates a list of requests for Twitter Advanced Search to scrape all historical Tweets
    from a list of Twitter handles and a given time frame.
    
    :param screen_names: the list of Twitter handles
    :param start: the start date of the time frame
    :param end: the end date of the time frame
    :param step: the step size of the dates
    :param date_format: the string format of the dates inputted and returned
    """
    for name in screen_names:
        dates = date_range(start=start, end=end, step=step, date_format=date_format)
        prev, current = next(dates), next(dates, None)
        while current is not None:
            yield f'from:{name} since:{prev} until:{current}'
            try:
                prev, current = current, next(dates)
            except StopIteration:
                break
    