import boto3
from time import gmtime, strftime

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
        options = []
        count = 1
        for k in selection:
            options.append(str(count) + ". " + str(k))
            count += 1

        orderDB.put_item(
            Item={
                'order_id': order_id,
                'menu_id': menu_id,
                'customer_name': customer_name,
                'customer_email': customer_email,
		'order_status': None,
                'selection': None,
                'size': None,
                'costs': None,
		'order_time': None

            }
        )
        msg = "Hi %s, please choose one of these selection:  %s" % (customer_name, ', '.join(options))

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
	    selections = menuItem.get('selection')
            options = []
            count = 1
            for k in size:
                options.append(str(count) + ". " + str(k))
                count += 1

            # Update selection in PizzaOrder table
            option = int(event.get("data").get("input"))

            orderDB.update_item(
                Key={
                    'order_id': order_id,
                },
                UpdateExpression='SET selection = :val',
                ExpressionAttributeValues={
                    ':val': selections[option]
                }
            )

            msg = "Which size do you want?:  %s" % ', '.join(options)
            return {
                'status': 200,
                'Message': msg
            }
	else:
            priceList = menuItem.get('price')
	    sizes = menuItem.get('size');
            size = int(event.get("data").get("input"))
	    order_time = strftime("%m-%d-%Y@%H:%M:%S", gmtime())
            # Update size and price in PizzaOrder table
            orderDB.update_item(
                Key={
                    'order_id': order_id,
                },
                UpdateExpression='SET size = :s, costs = :p, order_status = :status, order_time = :ot',
                ExpressionAttributeValues={
                    ':s': sizes[size],
                    ':p': priceList[size],
		    ':status': "processing",
                    ':ot': order_time
                }
           )
            msg = "Your order costs %s. We will email you when the order is ready. Thank you!" % str(priceList[size - 1])

            return {
                 'status': 200,
                 'Message': msg
            }
    elif httpMethod == "GET":
        order_id = event.get("param").get("order_id")
        print "Order id", order_id
	response = orderDB.get_item(
            Key={
                'order_id': order_id
            }
        )
        data = response['Item']
        return {
	    "status" : 200,
            "menu_id": data["menu_id"],
            "order_id": data["order_id"],
            "customer_name": data["customer_name"],
            "customer_email": data["customer_email"],
            "order_status":  data["order_status"],
            "order": {
		 "selection": data["selection"],
        	 "size": data["size"],
                 "costs": data["costs"],
                 "order_time": data["costs"]

	    }
        } 
