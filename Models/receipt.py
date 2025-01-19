import uuid

class Receipt:
    def __init__(self, receipt_json):
        assert self.validReceipt(receipt_json)
        self.retailer = receipt_json['retailer']
        self.purchase_date = receipt_json['purchaseDate']
        self.purchase_time = receipt_json['purchaseTime']
        self.items = receipt_json['items']
        self.total = receipt_json['total']
        self.id = str(uuid.uuid4())
        self.score = None

    def validReceipt(self, receipt_json):
        for key in ['retailer','purchaseDate','purchaseTime','items','total']:
            if key not in receipt_json:
                return False
        return True
