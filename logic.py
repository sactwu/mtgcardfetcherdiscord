import re
from scryfall import get_set_codes, fetch_card


def split_match(match):
    split_text = match.split('@')
    name = split_text[0].strip()
    set_codes = get_set_codes()
    fetch_type = 'image'
    extras = False
    set_code = ''
    for token in split_text[1:]:
        if token.lower().strip() in ['text', 'txt']:
            fetch_type = 'text'
        if token.lower().strip() in ['extras', 'extra', 'full']:
            extras = True
        if token.lower().strip() in set_codes:
            set_code = token.lower().strip()

    return name, fetch_type, extras, set_code


def get_queries(message):
    matches = re.findall("(?<=\\[\\[).*?(?=]])", message)
    queries = []
    for match in matches:
        name, fetch_type, extras, set_code = split_match(match)
        queries.append((name, fetch_type, extras, set_code))

    return queries


def fetch_cards(message):
    queries = get_queries(message)
    response = {
        'cards': []
    }
    for query in queries:
        (name, fetch_type, extras, set_code) = query
        card = fetch_card(name, fetch_type, extras, set_code)
        print(card)
        response_card = {
            'fetch_type': fetch_type,
            'items': [],
            'len': len(card)
        }
        if fetch_type == 'text':
            for item in card:
                print(item)
                response_card['items'].append(item)
        elif fetch_type == 'image':
            if len(card) == 1:
                item = card[0]
                print(item)
                response_card['items'] = item
            elif len(card) > 1:
                card = card[:10]
                for item in card:
                    print(item)
                    response_card['items'].append(item)

        response['cards'].append(response_card)
    return response



