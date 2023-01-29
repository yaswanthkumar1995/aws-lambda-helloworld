import boto3, csv, sys

iam = boto3.client('iam')

user_list = []
max_items = 100

users = iam.list_users(MaxItems=max_items)
while users:
    for user in users['Users']:
        # Get user permissions
        policies = iam.list_attached_user_policies(UserName=user['UserName'])['AttachedPolicies']
        policy_list = list(item['PolicyName'] for item in policies)

        # Get user groups
        groups = iam.list_groups_for_user(UserName=user['UserName'])
        groups_list = list(item['GroupName'] for item in groups['Groups'])

        # Construct user dict
        user_details ={
        'user': user['UserName'],
        'groups': ", ".join(groups_list) if groups_list else "N/A",
        'policies': ", ".join(policy_list) if policy_list else "None",
        'last_login': user.get('PasswordLastUsed'),
        'created': user['CreateDate'],
        }
        user_list.append(user_details)
        # Print progress marker because it may take awhile to complete
        sys.stdout.write("\r"+str(len(user_list)))
        sys.stdout.flush()

    marker = users.get('Marker')
    users = iam.list_users(MaxItems=max_items, Marker=marker) if marker else False

keys = user_list[0].keys()
with open('aws_users.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(user_list)
