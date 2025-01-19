import uuid
import re

class Receipt:
    def __init__(self, receipt_json):
        assert self.validReceipt(receipt_json)
        self.retailer = receipt_json['retailer']
        self.purchase_date = receipt_json['purchaseDate']
        self.purchase_time = receipt_json['purchaseTime']

        self.items = []
        for item in receipt_json['items']:
            self.items.append(ReceiptItem(item))
        self.total = receipt_json['total']
        self.id = str(uuid.uuid4())
        self.score = None

    def validReceipt(self, receipt_json):
        validPatterns = {
            'retailer': r'^[\w\s\-&]+$',
            'purchaseDate': r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$',
            'purchaseTime': r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
            'total': r'^\d+\.\d{2}$',
        }
        for key in ['retailer','purchaseDate','purchaseTime','items','total']:
            if key not in receipt_json:
                return False
            if key in validPatterns and not re.match(validPatterns[key], receipt_json[key]):
                return False
        return isinstance(receipt_json['items'], list) and len(receipt_json['items']) > 0

class ReceiptItem:
    def __init__(self, item_data):
        assert self.validItem(item_data)
        self.shortDescription = item_data['shortDescription']
        self.price = item_data['price']

    def validItem(self, item_data):
        validPatterns = {
            'shortDescription': r'^[\w\s\-]+$',
            'price': r'^\d+\.\d{2}$',
        }
        for key in ['shortDescription','price']:
            if key not in item_data:
                return False
            if not re.match(validPatterns[key], item_data[key]):
                return False
        return True