import boto3

def handler(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    menuDB = dynamodb.Table('PizzaMenu')

    httpMethod = event.get('httpMethod')
    data = event.get('data')

    if httpMethod == "POST":
        menuDB.put_item(
            Item={
                "menu_id": data["menu_id"],
                "store_name": data["store_name"],
                "selection": data["selection"],
                "size": data["size"],
                "price": data["price"],
                "store_hours": data["store_hours"]
            }
        )

        return {
            "status": 200
        }
    elif httpMethod == "GET":
        menu_id = event.get("param").get("menu_id")
        response = menuDB.get_item(
            Key={
                'menu_id': menu_id
            }
        )
        data = response['Item']
        return {
            "menu_id": data["menu_id"],
            "store_name": data["store_name"],
            "selection": data["selection"],
            "size": data["size"],
            "price": data["price"],
            "store_hours": data["store_hours"]
        }
    elif httpMethod == "PUT":
        menu_id = event.get("param").get("menu_id")
        selection = event.get("data").get("selection")
        menuDB.update_item(
            Key={
                'menu_id': menu_id,
            },
            UpdateExpression='SET selection = :val',
            ExpressionAttributeValues={
                ':val': selection
            }
        )
        return {
            "status": 200,
            "response": {
                "menu_id": menu_id,
                "selection": selection
            }
        }
    elif httpMethod == "DELETE":
        menu_id = event.get("param").get("menu_id")
        menuDB.delete_item(
            Key={
                'menu_id': menu_id
            }
        )
        return {
            "status": 200
        }
