import pprint

pp = pprint.PrettyPrinter(indent=4)


def parse_recipes(filename, encoding='utf-8', strict_mode=True):
    """
    This function can work in two modes:

    1. Strict mode - when file structure should always be correct, except some redundant whitespaces allowed.
    Any errors in this mode will lead to return empty dict.

    2. Flex mode - when allowed additional line breaks, incorrect or absent ingredients quantity, even
    allowed line break instead of ingredients quantity. Also allowed mistakes in ingredient quantity (i.e.
    if we put instead "2" word "two"). The main condition that recipe name must precede ingredients list.
    """
    result = {}
    # some checks skipped, so errors in file structure will lead to return an empty dict
    if strict_mode:
        with open(filename, encoding=encoding) as recipes:
            line = recipes.readline()
            recipe_name = None
            ingred_count = -1
            while line != '':
                line = line.strip()
                if recipe_name is None:
                    recipe_name = line
                    result[recipe_name] = []
                    line = recipes.readline()
                    continue
                # foll condition should execute immediately after finding recipe name (on next iteration)
                if ingred_count < 0:
                    try:
                        ingred_count = int(line)
                    except ValueError as e:
                        return {}
                # foll condition means that we reached the end of ingredients list
                # so we need to reset markers and pass one empty line
                elif ingred_count == 0:
                    recipe_name = None
                    ingred_count = -1
                else:
                    tmp_dict = dict(zip(
                        ['ingredient_name', 'quantity', 'measure'],
                        [x.strip() for x in line.split('|')]))
                    try:
                        tmp_dict['quantity'] = int(tmp_dict.setdefault('quantity', 0))
                    except ValueError as e:
                        return {}
                    result[recipe_name].append(tmp_dict)
                    ingred_count -= 1
                line = recipes.readline()
    # if we working in flex-mode
    else:
        with open(filename, encoding=encoding) as recipes:
            line = recipes.readline()
            # using the cursor to memorize the position
            # set cursor for search of destination
            cursor = 'recipe_name'
            recipe_name = None
            while line != '':
                line = line.strip()
                # if we searching for recipe_name and found non-empty string
                if cursor == 'recipe_name' and len(line) > 0:
                    recipe_name = line
                    result[line] = []
                    cursor = 'ingred_count'
                    line = recipes.readline()
                    continue
                if cursor == 'ingred_count':
                    cursor = 'ingredients'
                    # in flex mode we don't need ingredients quantity
                    # so check if we found not ingredients and move to next step
                    tmp_list = line.split('|')
                    if len(tmp_list) <= 1:
                        line = recipes.readline()
                    continue
                if cursor == 'ingredients':
                    tmp_list = line.split('|')
                    # if no more ingredients, lets assume that we've got a recipe name
                    if len(tmp_list) != 3:
                        cursor = 'recipe_name'
                        recipe_name = None
                        # if empty string with caret return was found, let's move to next line
                        if line == '':
                            line = recipes.readline()
                        continue
                    tmp_dict = dict(zip(
                        ['ingredient_name', 'quantity', 'measure'],
                        [x.strip() for x in tmp_list]))
                    try:
                        tmp_dict['quantity'] = int(tmp_dict.setdefault('quantity', 0))
                    except ValueError as e:
                        # do nothing, and leave as is
                        pass
                    result[recipe_name].append(tmp_dict)
                line = recipes.readline()
    return result


def get_shop_list_by_dishes(dishes, person_count, filename='recipes.txt'):
    """
    This function will take list of dishes and persons quantity
    to make shopping list of ingredients with total quantity of them
    """
    result = {}
    for dish in dishes:
        # let's find requested dish in recipes
        ingred_list = parse_recipes(filename)[dish]
        for item in ingred_list:
            ingred_name = item['ingredient_name']
            ingred_found = result.setdefault(ingred_name,
                                             {'measure': item['measure'], 'quantity': 0})
            ingred_found['quantity'] = ingred_found['quantity'] + item['quantity']
            result[ingred_name] = ingred_found
    return result


print('Нормальный рецепт:')
cook_book = parse_recipes('recipes.txt')
pp.pprint(cook_book)

print('\nИспорченный рецепт:')
cook_book = parse_recipes('recipes_bad.txt', 'utf-8', False)
pp.pprint(cook_book)

print('\nСписок покупок:')
pp.pprint(get_shop_list_by_dishes(['Фахитос', 'Омлет'], 2))
