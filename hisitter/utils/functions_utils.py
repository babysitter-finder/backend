""" Functions to handle differents issues or special cases. """

def time_cost_treatment(service_start, service_end, cost_of_service):
    """ Function that helps to treatment the delta of dates. """
    timedelta = service_end - service_start
    days_to_hours = timedelta.days * 24
    seconds_to_hours = timedelta.seconds//3600
    total_hours = days_to_hours + seconds_to_hours
    cost_of_service = float(cost_of_service)
    return (total_hours * cost_of_service, timedelta)