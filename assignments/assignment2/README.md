#### Requirements
Building a pizza ordering system using AWS Lambda for handling business logic, API Gateway for REST interface, and DynamoDB for data persistence.

#### Output

##### I. Pizza Menu CRUD APIs

1. POST /menu

```json
curl --header "Content-Type:application/json" \
     --request POST \
     --data '{ 
        "menu_id": "1",
        "store_name": "Pizza Hut",
        "selection": [
          "Cheese",
          "Pepperoni"
        ],
        "size": [
          "Slide", "Small", "Medium", "Large", "X-Large"
        ],
        "price": [
          "3.50", "7.00", "10.00", "15.00", "20.00"
        ],
        "store_hours": {
          "Mon": "10am-10pm",
          "Tue": "10am-10pm",
          "Wed": "10am-10pm",
          "Thu": "10am-10pm",
          "Fri": "10am-10pm",
          "Sat": "11am-12pm",
          "Sun": "11am-12pm"
      }
  }' \
  https://as58vdws4e.execute-api.us-west-2.amazonaws.com/v1/menu
````
```json
{
  "status": 200
}
```

2. DELETE /menu/{menu-id}

````json
curl --header "Content-Type:application/json" \
     --request DELETE \
     https://as58vdws4e.execute-api.us-west-2.amazonaws.com/v1/menu/1
````

```json
{
  "status": 200
}
```

3. PUT /menu/{menu-id}

````json
curl --header "Content-Type:application/json" \
     --request PUT \
     --data '{
        "selection": ["Cheese","Pepperoni","Vegetable"] 
     }' \
     https://as58vdws4e.execute-api.us-west-2.amazonaws.com/v1/menu/1
````

```json
{
  "status": 200, 
  "response": {
    "menu_id": "1", 
    "selection": ["Cheese", "Pepperoni", "Vegetable"]
  }
}
```

4. GET /menu/{menu-id}

````json
curl --header "Content-Type:application/json" \
     --request GET \
     https://as58vdws4e.execute-api.us-west-2.amazonaws.com/v1/menu/1
````

```json
{
  "menu_id": "1", 
  "selection": ["Cheese", "Pepperoni", "Vegetable"], 
  "price": ["3.50", "7.00", "10.00", "15.00", "20.00"], 
  "store_hours": {
    "Wed": "10am-10pm", 
    "Sun": "11am-12pm", 
    "Fri": "10am-10pm", 
    "Tue": "10am-10pm", 
    "Mon": "10am-10pm", 
    "Thu": "10am-10pm", 
    "Sat": "11am-12pm"
  }, 
  "store_name": "Pizza Hut", 
  "size": ["Slide", "Small", "Medium", "Large", "X-Large"]
}
```

##### II. Pizza Order Processing APIs

1. POST /order

````json
curl --header "Content-Type:application/json" \
     --request POST \
     --data '{
      "menu_id": "1", 
      "order_id": "123", 
      "customer_name": "John Smith",
      "customer_email": "foobar@gmail.com"
     }' \
     https://z9ua29uer6.execute-api.us-west-2.amazonaws.com/v1/order
````

```json
{
  "status": 200, 
  "Message": "Hi John Smith, please choose one of these selection:  1. Cheese, 2. Pepperoni, 3. Vegetable"
}
```

2. PUT /order/{order_id}

````json
curl --header "Content-Type:application/json" \
     --request PUT \
     --data '{
      "input": "1"
     }' \
     https://z9ua29uer6.execute-api.us-west-2.amazonaws.com/v1/order/123
````

```json
{
  "status": 200, 
  "Message": "Which size do you want?:  1. Slide, 2. Small, 3. Medium, 4. Large, 5. X-Large"
}
```

2. PUT /order/{order_id}
````json
curl --header "Content-Type:application/json" \
     --request PUT \
     --data '{
      "input": "1"
     }' \
     https://z9ua29uer6.execute-api.us-west-2.amazonaws.com/v1/order/123
````

```json
{
  "status": 200, 
  "Message": "Your order costs 15.00. We will email you when the order is ready. Thank you!"
}
```

3. GET /order/{order-id}

````json
curl --header "Content-Type:application/json" \
     --request GET \
     https://z9ua29uer6.execute-api.us-west-2.amazonaws.com/v1/order/123
````

```json
{
  "status": 200, 
  "menu_id": "1", 
  "customer_email": "foobar@gmail.com", 
  "order_id": "123", 
  "order_status": "processing", 
  "order": {
      "selection": "Pepperoni", 
      "costs": "20.00", 
      "order_time": "20.00", 
      "size": "X-Large"
  }, 
  "customer_name": "John Smith"
}
````


