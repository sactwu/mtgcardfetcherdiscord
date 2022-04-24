import scrython


def get_card_by_name(name, set_code=''):
    card = scrython.cards.Named(fuzzy=name, set=set_code)
    return card


def get_card_by_number(set_code='', collector_number=''):
    card = scrython.cards.Collector(code=set_code, collector_number=collector_number)
    return card


def get_card_image(card):
    return card.image_uris(image_type='normal')


def get_set_codes():
    sets = scrython.sets.Sets()
    set_codes = set()
    for i in range(sets.data_length()):
        set_codes.add(sets.data(index=i, key='code'))
    return set_codes


def get_all_cards_values(card, extras):
    # print(card.scryfallJson)
    cards_values = []
    if extras:
        if 'all_parts' in card.scryfallJson:
            for part in card.scryfallJson['all_parts']:
                if part['name'] == card.name():
                    cards_values.append(get_card_values(card))
                else:
                    cards_values.append(get_part_values(part))
    elif 'card_faces' in card.scryfallJson:
        for part in card.scryfallJson['card_faces']:
            if part['name'] == card.name():
                cards_values.append(get_card_values(card))
            else:
                cards_values.append(get_part_values(part))
    else:
        cards_values.append(get_card_values(card))
    return cards_values


def get_card_values(card):
    values = dict()
    values['Name'] = card.name()
    values['Cost'] = card.mana_cost()
    values['Type'] = card.type_line()
    values['Text'] = card.oracle_text()
    values['Scryfall Link'] = card.scryfall_uri()
    if 'Creature' in values['Type']:
        values['Power/Toughness'] = f'{card.power()}/{card.toughness()}'
    if 'Planeswalker' in values['Type']:
        values['Loyalty'] = card.loyalty()
    price = card.prices('eur')
    if price:
        values['Price'] = price + '€'
    values['Image'] = card.image_uris(image_type='normal')
    return values


def get_part_values(part):
    values = dict()
    values['Name'] = part['name']
    values['Type'] = part['type_line']
    if part['object'] == 'related_card':
        values = get_card_values(scrython.cards.Id(id=part['id']))
    else:
        values['Cost'] = part['mana_cost']
        values['Text'] = part['oracle_text']
        if 'Creature' in values['Type']:
            values['Power/Toughness'] = f'{part["power"]}/{part["toughness"]}'
        if 'Planeswalker' in values['Type']:
            values['Loyalty'] = part['loyalty']
        values['Image'] = part['image_uris']['normal']
    return values


def fetch_card(name, fetch_type, extras, set_code, collector_number):
    # try:
    if name:
        card = get_card_by_name(name, set_code)
    elif set_code and collector_number:
        card = get_card_by_number(set_code, collector_number)
    else:
        return ['please provide either a card name or both set code and collector number']
    cards_values = get_all_cards_values(card, extras)
    if fetch_type == 'image':
        response = []
        for values in cards_values:
            response.append(values["Scryfall Link"])
            response.append(values["Image"])
            print('fetched image from scryfall')
        return response
    if fetch_type == 'text':
        response = ''
        for values in cards_values:
            for value in values:
                if not value == 'Image':
                    response += f'{value}: {values[value]}\n'
            if len(values) > 1:
                response += '----------------\n'
            print('fetched text from scryfall')
        return [response]
    # except:
    #    return ['error']
