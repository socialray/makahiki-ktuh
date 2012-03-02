"""template tag definition for Prize page"""
from django import template

register = template.Library()


def user_tickets(raffle_prize, user):
    """return the allocate ticket for user"""
    return raffle_prize.allocated_tickets(user)


def user_odds(raffle_prize, user):
    """return the user odd for the prize"""
    total_tickets = raffle_prize.allocated_tickets()
    if total_tickets == 0:
        return "0%"

    tickets = raffle_prize.allocated_tickets(user)
    odds = (float(tickets) * 100.0) / float(total_tickets)
    return "%0.1f%%" % (odds,)

register.filter("user_tickets", user_tickets)
register.filter("user_odds", user_odds)

# Borrowed from http://djangosnippets.org/snippets/552/
# This locale setting uses the environment's locale setting.
import locale

#locale.setlocale(locale.LC_ALL, settings.LOCALE_SETTING)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


@register.filter()
def currency(value):
    """return the currency character from the locale"""
    return locale.currency(value, grouping=True)
