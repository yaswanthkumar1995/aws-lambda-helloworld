import boto3, csv, sys

session = boto3.Session(profile_name='yas')
iam = session.client('iam')

max_items = 100
groups = iam.list_groups()

group_list =[]

while groups:        #MaxItems=max_items,GroupName=groupname)
  for group in groups['Groups']:
    group_details = iam.get_group(GroupName=group['GroupName'])
    #print(group_details)
    #print(group['GroupName'])
    user_list = list(user['UserName'] for user in group_details['Users'])
   #print(user_list)

    InlinePolicies = iam.list_group_policies(GroupName=group['GroupName'])['PolicyNames']
    #print(InlinePolicies)

    ManagedPolicies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
    managed_policy_list = list(item['PolicyName']for item in ManagedPolicies)
    #print(ManagedPolicies)
    grouplist = {
                'group': group['GroupName'],
                'users': ",".join(user_list) if user_list else "N/A",
                'InlinePolicies': ",".join(InlinePolicies) if InlinePolicies else None,
                'managedpolicies': ",".join(managed_policy_list) if managed_policy_list else None
                }

    group_list.append(grouplist)
    #print(group_list)

    sys.stdout.write("\r"+str(len(group_list)))
    sys.stdout.flush()


  marker = groups.get('Marker')
  groups = iam.list_groups(MaxItems=max_items, Marker=marker) if marker else False

keys = group_list[0].keys()


#print(group_list[0])
with open('aws_group_users.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(group_list)
