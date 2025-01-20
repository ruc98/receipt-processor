from receipt import Receipt

def validData():
    return {
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ],
        "total": "35.35"
    }

def testValidRetailer():
    valid_retailers = ["Walmart", "Best Buy", "M&M Corner Market", "Trader Joe's", "Whole-Foods Market"]
    for retailer in valid_retailers:
        data = validData()
        data["retailer"] = retailer
        assert Receipt(data).retailer == retailer

def testInvalidRetailer():
    invalid_retailers = ["Walmart!", "Best*Buy", "", "Trader@Joe's", "Whole_Foods_Market"]
    for retailer in invalid_retailers:
        data = validData()
        data["retailer"] = retailer
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def testValidPurchaseDate():
    valid_dates = ["2022-01-01", "1999-12-31", "2024-02-29", "2023-06-15", "2000-09-30"]
    for date in valid_dates:
        data = validData()
        data["purchaseDate"] = date
        assert Receipt(data).purchaseDate == date

def testInvalidPurchaseDate():
    invalid_dates = ["2022-13-01", "2022-00-10", "2022-01-32", "22-01-01", "2022/01/01"]
    for date in invalid_dates:
        data = validData()
        data["purchaseDate"] = date
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def testValidPurchaseTime():
    valid_times = ["00:00", "13:45", "9:05", "23:59", "02:30"]
    for time in valid_times:
        data = validData()
        data["purchaseTime"] = time
        assert Receipt(data).purchaseTime == time

def testInvalidPurchaseTime():
    invalid_times = ["24:00", "12:60", "3:5", "-03:45", "99:99"]
    for time in invalid_times:
        data = validData()
        data["purchaseTime"] = time
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def testValidTotal():
    valid_totals = ["0.00", "10.50", "999.99", "5.00", "12345.67"]
    for total in valid_totals:
        data = validData()
        data["total"] = total
        assert Receipt(data).total == total

def testInvalidTotal():
    invalid_totals = ["10.5", "10,50", "-10.50", "10.505", "abc.def"]
    for total in invalid_totals:
        data = validData()
        data["total"] = total
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def testValidItems():
    data = validData()
    receipt = Receipt(data)
    assert len(receipt.items) == 5

def testInvalidItems():
    data = validData()
    data["items"] = []
    try:
        Receipt(data)
        assert False
    except AssertionError:
        assert True

def testValidShortDescription():
    valid_descriptions = [
        "Mountain Dew",
        "Doritos Nacho-Cheese",
        "Knorr Creamy Chicken",
        "12 Pack",
        "Vitamin-C Supplement"
    ]
    for desc in valid_descriptions:
        data = validData()
        data["items"][0]["shortDescription"] = desc
        assert Receipt(data).items[0].shortDescription.strip() == desc

def testInvalidShortDescription():
    invalid_descriptions = [
        "Mountain_Dew",
        "Doritos@Cheese",
        "Protein*Bar",
        "",
        "Super-Drink!"
    ]
    for desc in invalid_descriptions:
        data = validData()
        data["items"][0]["shortDescription"] = desc
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def testValidPrice():
    valid_prices = ["0.00", "10.50", "999.99", "5.00", "12345.67"]
    for price in valid_prices:
        data = validData()
        data["items"][0]["price"] = price
        assert Receipt(data).items[0].price == price

def testInvalidPrice():
    invalid_prices = ["10.5", "10,50", "-10.50", "10.505", "abc.def"]
    for price in invalid_prices:
        data = validData()
        data["items"][0]["price"] = price
        try:
            Receipt(data)
            assert False
        except AssertionError:
            assert True

def runTests():
    testValidRetailer()
    testInvalidRetailer()
    testValidPurchaseDate()
    testInvalidPurchaseDate()
    testValidPurchaseTime()
    testInvalidPurchaseTime()
    testValidTotal()
    testInvalidTotal()
    testValidItems()
    testInvalidItems()
    testValidShortDescription()
    testInvalidShortDescription()
    testValidPrice()
    testInvalidPrice()
    print("All tests passed.")

if __name__ == '__main__':
    runTests()
