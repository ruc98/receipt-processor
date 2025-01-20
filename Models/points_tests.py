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

testPoints = 6 + 0 + 0 + 5*2 + 3 + 3 + 6
def testValidData():
    data = validData()
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints

def testRule1():
    data = validData()
    data["retailer"] = "Target123"
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints + 3

def testRule2():
    data = validData()
    data["total"] = "40.00"
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints + 50 + 25

def testRule3():
    data = validData()
    data["total"] = "25.25"
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints + 25

def testRule4():
    data = validData()  
    data["items"].append({"shortDescription": "Item1", "price": "1.00"})
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints + 5

def testRule5():
    data = validData()
    data["items"][0] = {"shortDescription": "ABCDEF", "price": "12.20"}
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints + 3
    
    data["items"][0] = {"shortDescription": "ABCDE", "price": "12.20"}
    receipt = Receipt(data)
    assert receipt.getPoints()  == testPoints

def testRule6():
    data = validData()
    data["purchaseDate"] = "2022-01-02"
    receipt = Receipt(data)
    assert receipt.getPoints() == testPoints - 6

def testRule7():
    valid_times = ["14:01", "15:45", "15:59"]
    for time in valid_times:
        data = validData()
        data["purchaseTime"] = time
        receipt = Receipt(data)
        assert receipt.getPoints() == testPoints + 10

    invalid_times = ["00:00", "13:45", "14:00", "16:00", "16:01", "02:30"]
    for time in invalid_times:
        data = validData()
        data["purchaseTime"] = time
        receipt = Receipt(data)
        assert receipt.getPoints() == testPoints

def runTests():
    testValidData()
    testRule1()
    testRule2()
    testRule3()
    testRule4()
    testRule5()
    testRule6()
    testRule7()
    print("All tests passed.")

if __name__ == '__main__':
    runTests()
