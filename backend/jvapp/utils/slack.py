
class SlackException(Exception):
    pass


def raise_slack_exception_if_error(slack_response):
    if not slack_response['ok']:
        raise SlackException(slack_response['error'])
