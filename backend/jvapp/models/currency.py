from django.db import models

__all__ = ('Currency',)

currencies = [
    'AED', 'ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'CZK', 'DKK', 'EUR', 'GBP',
    'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD',
    'PEN', 'PHP', 'PLN', 'PYG', 'RON', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'UAH', 'USD',
    'UYU', 'VND', 'ZAR'
]

currency_lookup = {
    'د.إ': 'AED',
    'R$': 'BRL',
    'Fr.': 'CHF',
    '元': 'CNY',
    'Kč': 'CZK',
    'kr': 'DKK',
    '€': 'EUR',
    '£': 'GBP',
    'kn': 'HRK',
    'Ft': 'HUF',
    'Rp': 'IDR',
    '₪': 'ILS',
    '₹': 'INR',
    '¥': 'JPY',
    '円': 'JPY',
    '₩': 'KRW',
    'RM': 'MYR',
    'S/.': 'PEN',
    '₱': 'PHP',
    'zł': 'PLN',
    '₲': 'PYG',
    'lei': 'RON',
    '﷼': 'SAR',
    '฿': 'THB',
    '₺': 'TRY',
    '₴': 'UAH',
    '$': 'USD',
    '₫': 'VND',
    'R': 'ZAR',
}


class Currency(models.Model):
    name = models.CharField(max_length=20, unique=True)
    symbol = models.CharField(max_length=5)
