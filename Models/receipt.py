import uuid
import re

class Receipt:
    """
    The Receipt class represents a purchase receipt and provides functionality to calculate reward points.

    Attributes:
        id (str): A unique identifier assigned to the receipt.
        retailer (str): The name of the retailer.
        purchaseDate (str): The purchase date in the format YYYY-MM-DD.
        purchaseTime (str): The purchase time in the format HH:MM or H:MM.
        items (list): A list of items included in the purchase.
        total (str): The total purchase amount in the format (D+).DD.
        points (int): The reward points calculated based on the receipt details.
    """
    def __init__(self, receiptData):
        """
        Creates a Receipt object from a provided JSON object. 
        Required fields: retailer, purchaseDate, purchaseTime, items and total.
        """

        assert self.validReceipt(receiptData)
        self.id = str(uuid.uuid4())
        self.retailer = receiptData['retailer']
        self.purchaseDate = receiptData['purchaseDate']
        self.purchaseTime = receiptData['purchaseTime']

        self.items = []
        for item in receiptData['items']:
            self.items.append(ReceiptItem(item))
        self.total = receiptData['total']
        self.points = self.computePoints()

    def validReceipt(self, receiptData):
        """
        Ensures that the receipt fields match the specified regex pattern for the corresponding field.
        """
        validPatterns = {
            'retailer': r'^[\w\s\-&]+$',
            'purchaseDate': r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$',
            'purchaseTime': r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
            'total': r'^\d+\.\d{2}$',
        }
        for key in ['retailer','purchaseDate','purchaseTime','items','total']:
            if key not in receiptData:
                return False
            if key in validPatterns and not re.match(validPatterns[key], receiptData[key]):
                return False
        return isinstance(receiptData['items'], list) and len(receiptData['items']) > 0
    
    def computePoints(self):
        """
        Calculates the reward points earned from receipt details.
        """
        points = 0

        # One point for every alphanumeric character in the retailer name.
        points += sum(ch.isalnum() for ch in self.retailer)

        # 50 points if the total is a round dollar amount with no cents.
        cents = int(self.total.split(".")[1])
        if cents == 0:
            points += 50

        # 25 points if the total is a multiple of 0.25.
        if cents % 25 == 0:
            points += 25

        # 5 points for every two items on the receipt.
        points += 5 * (len(self.items) // 2)

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 
        # and round up to the nearest integer. The result is the number of points earned.
        for item in self.items:
            trimmedLength = len(item.shortDescription.strip())
            if trimmedLength % 3 == 0:
                points += int(float(item.price) * 0.2) + 1

        # 6 points if the day in the purchase date is odd.
        day = int(self.purchaseDate.split("-")[2])
        if day % 2:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        hours, mins = self.purchaseTime.split(":")
        totalMins = int(hours) * 60 + int(mins)
        if 14 * 60 < totalMins < 16 * 60:
            points += 10

        return points

    def getPoints(self):
        """
        Returns the calculated reward points for the receipt.
        """
        return self.points
    
    def getId(self):
        """
        Returns the generated id for the receipt.
        """
        return self.id
    
class ReceiptItem:
    """
    The ReceiptItem class represents a purchased item with relevant details.

    Attributes:
        shortDescription (str): A brief description of the item.
        price (str): The item's price in the format (D+).DD.
    """
    def __init__(self, itemData):
        """
        Creates a recepit item object given the JSON object.
        Required fields: shortDescription, price
        """
        assert self.validItem(itemData)
        self.shortDescription = itemData['shortDescription']
        self.price = itemData['price']

    def validItem(self, itemData):
        """
        Ensures that the item fields match the specified regex pattern for the corresponding field.
        """
        validPatterns = {
            'shortDescription': r'^[\w\s\-]+$',
            'price': r'^\d+\.\d{2}$',
        }
        for key in ['shortDescription','price']:
            if key not in itemData:
                return False
            if not re.match(validPatterns[key], itemData[key]):
                return False
        return True