# Receipt Processor

## Requirements
1. [Python3](https://docs.python-guide.org/starting/install3/linux/)

## Instructions to run the code
Run the below docker commands to run the solution.

`docker build -t receipt-processor .`

`docker run -p 127.0.0.1:8000:8000 receipt-processor`

This will run the server code and will be serving the requests at `127.0.0.1:8000` (or `localhost:8000`).

(Optional) You can run the solution using Python
`python3 receipt_server.py`

## Additional Information
1. Made a slight adjustment to the given retailer pattern `^[\w\s\-&]+$`. This pattern does not consider retailers that have appostrophe in their name, such as "Trader Joe's". To handle this, I changed the regex pattern to `^[\w\s\-\'&]+$`.
2. I have added test cases that tests for valid and invalid receipt data in `receipt_tests.py`. Also added additional tests for each of the rules used to compute the reward points so that we can have full test coverage. These tests are in the file `points_tests.py`.
3. The receipt information is converted from the input JSON into the Receipt model. Created a separate ReceiptItem class to store the item information.
4. The reward points are precomputed and stored in the Receipt class during the POST request as against computing it on-the-fly during the GET request.
5. Used in-memory key-value store (dictionary in Python) to store the input receipts.
6. Used Universally Unique Identifier to generate IDs
