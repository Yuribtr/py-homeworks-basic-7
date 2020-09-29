import pprint

pp = pprint.PrettyPrinter(indent=4)


def parse_recipes(filename, encoding='utf-8', strict_mode=True):
    result = {}
    # some checks skipped, so errors in file structure will lead to return an empty dict
    if strict_mode:
        with open(filename, encoding=encoding) as recipes:
            line = recipes.readline()
            recipe_name = None
            ingrid_count = -1
            while line != '':
                line = line.strip()
                if recipe_name is None:
                    recipe_name = line
                    result[recipe_name] = []
                    line = recipes.readline()
                    continue
                if ingrid_count < 0:
                    try:
                        ingrid_count = int(line)
                    except ValueError as e:
                        return {}
                elif ingrid_count == 0:
                    recipe_name = None
                    ingrid_count = -1
                else:
                    tmp_dict = dict(zip(
                        ['ingredient_name', 'quantity', 'measure'],
                        [x.strip() for x in line.split('|')]))
                    try:
                        tmp_dict['quantity'] = int(tmp_dict.setdefault('quantity', 0))
                    except ValueError as e:
                        return {}
                    result[recipe_name].append(tmp_dict)
                    ingrid_count -= 1
                line = recipes.readline()
    else:
        pass
    return result


cook_book = parse_recipes('recipes.txt')
pp.pprint(cook_book)
