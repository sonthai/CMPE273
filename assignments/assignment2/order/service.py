import boto3

def handler(event, context):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    orderDB = dynamodb.Table('PizzaOrder')
    menuDB = dynamodb.Table('PizzaMenu')


    httpMethod = event.get('httpMethod')
    data = event.get('data')

    if httpMethod == 'POST':
        order_id = data['order_id']
        customer_name = data['customer_name']
        customer_email = data['customer_email']

        menu_id = data['menu_id']

        menuData = menuDB.get_item(
            Key = {
                'menu_id': menu_id
            }
        )

        item = menuData['Item']
        selection = item.get('selection')
        options = ''
        count = 1
        for k in selection:
            options += str(count) + "." + str(k) + ' '
            count += 1

        orderDB.put_item(
            Item={
                'order_id': order_id,
                'menu_id': menu_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'selection': None,
                'size': None,
                'price': None

            }
        )
        msg = "Hi %s please choose one of these selection:  %s" % (customer_name, options)

        return {
            'status': 200,
            'Message': msg
        }
    elif httpMethod == 'PUT':
        order_id = event.get("param").get("order_id")
        orderItem = orderDB.get_item(Key={'order_id': order_id}).get('Item')
        pizzaSelection = orderItem.get("selection")

        menu_id = orderItem.get('menu_id')
        menuItem = menuDB.get_item(Key={'menu_id': menu_id}).get('Item')

        if pizzaSelection == None:
            size = menuItem.get('size')

            options = ''
            count = 1
            for k in size:
                options += str(count) + "." + str(k) + ' '
                count += 1

            # Update selection in PizzaOrder table
            option = event.get("data").get("input")

            orderDB.update_item(
                Key={
                    'order_id': order_id,
                },
                UpdateExpression='SET selection = :val',
                ExpressionAttributeValues={
                    ':val': option
                }
            )

            msg = "Which size do you want?:  %s" % options
            return {
                'status': 200,
                'Message': msg
            }
        else:
            priceList = menuItem.get('price')
            size = int(event.get("data").get("input"))

            # Update size and price in PizzaOrder table
            orderDB.update_item(
                Key={
                    'order_id': order_id,
                },
                UpdateExpression='SET size = :s, price = :p',
                ExpressionAttributeValues={
                    ':s': size,
                    ':p': priceList[size]
                }
            )

            msg = "Your order costs %s. We will email you when the order is ready. Thank you!" % str(priceList[size - 1])

            return {
                'status': 200,
                'Message': msg
            }








