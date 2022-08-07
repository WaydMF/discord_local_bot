import boto3

client = boto3.client('dynamodb', region_name="eu-west-2")


def get_prefixes(table_name, guild_id):
    response = client.get_item(
        TableName=table_name,
        Key={
            "GuildID": {
                'N': guild_id
            }
        }
    )

    if response.get('ResponseMetadata').get('HTTPStatusCode') != 200:
        print(f"Error occurred during getting prefixes for {guild_id} guild")

    if 'Item' in response:
        return response.get('Item').get('prefixes').get('SS')
    else:
        return None


def add_prefixes(table_name, guild_id, add_prefixes_list):

    if isinstance(add_prefixes_list, str):
        add_prefixes_list = [add_prefixes_list]
    old_prefixes = get_prefixes(table_name, guild_id)

    new_prefixes = set(old_prefixes)
    new_prefixes.update(add_prefixes_list)

    if len(old_prefixes) == 0:
        response = client.put_item(
            TableName=table_name,
            Item={
                "GuildID": {
                    'N': guild_id
                },
                "PrefixesSet": {
                    'SS': new_prefixes
                }
            }
        )
    else:
        response = client.update_item(
            TableName=table_name,
            Key={
                "GuildID": {
                    'N': guild_id
                },
                "PrefixesSet": {
                    'SS': new_prefixes
                }
            }
        )

    if response.get('ResponseMetadata').get('HTTPStatusCode') != 200:
        print(f"Error occurred during getting prefixes for {guild_id} guild")


def remove_prefixes(table_name, guild_id, rm_prefixes):

    if isinstance(rm_prefixes, str):
        rm_prefixes = [rm_prefixes]
    old_prefixes = get_prefixes(table_name, guild_id)

    new_prefixes = old_prefixes.difference(rm_prefixes)

    response = client.update_item(
        TableName=table_name,
        Key={
            "GuildID": {
                'N': guild_id
            },
            "PrefixesSet": {
                'SS': new_prefixes
            }
        }
    )
