import requests
import json
from config  import keys
class ConvExept(Exception):
    pass

class Conv:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvExept(f'Невозможно перевети одинаковые валюты {quote}')
    
        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvExept(f'Не удалось обработать валюту {base}')
    
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvExept(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvExept(f'Не удалось обработать колличество {amount}')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_tiker}&tsyms={quote_tiker}')
        text = json.loads(r.content)[keys[quote]]
        summ = float(text) * int(amount)
        
        return summ
       