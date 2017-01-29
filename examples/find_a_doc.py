import sys
from wit import Wit

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

# Quickstart example
# See https://wit.ai/ar7hur/Quickstart

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])


def get_doctors(request):
    context = request['context']
    entities = request['entities']

    search_term = first_entity_value(entities, 'doc_type')
    if not search_term: search_term = first_entity_value(entities, 'contact')
    if search_term:
        context['search_term'] = search_term
        #this should be the result of the api call
        #a text version can be added for display and the list itself can 
        #store unique id's, as this will help when the user asks for 
        #description
        context['doctors'] = ['Rajeev Sharma', 'Anju Bhasin', 'Anil Gupta'] 
    return context

def get_details(request):
    context = request['context']
    entities = request['entities']

    name = first_entity_value(entities, 'contact')
    if not name:
        print(entities)
        index = first_entity_value(entities, 'number')
        #have some security checks to make sure index is valid
        print (context)
        name = context['doctors'][index - 1]
    #this should be an api call using name and search_term
    context['name'] = name
    context['description'] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    return context


actions = {
    'send': send,
    'findDoctors': get_doctors,
    'getDetails': get_details
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
