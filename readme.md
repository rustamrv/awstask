1) POST REST API lambda aws
   > Link:
   ```
   https://6b3va08d4j.execute-api.us-east-1.amazonaws.com/dev/point  
   ```
   > Body example instance list
    ```
    {
        "urls": ["https://en.wikipedia.org/wiki/Wikipedia",
            "https://eu-west-1.console.aws.amazon.com/"]
    }
   ```
   > Or body instance str
   ```
   {
        "urls": "https://en.wikipedia.org/wiki/Wikipedia"
    }
   ```