def tree_maker(part_list):
    listem = part_list
    temp = []

    for child in listem:
        if len(child) == 2 and type(child[1]) == float:
            temp.append(child)
    for eleman in temp:
        if eleman in listem:
            listem.remove(eleman)

    def helper_tree_maker1(eleman, price,  updated_part_list):
        for sub_list in updated_part_list:
            for sub_sub_list in sub_list:
                if type(sub_sub_list) == tuple and (eleman == sub_sub_list[1]):
                    miktar = sub_sub_list[0]
                    sub_list[sub_list.index(sub_sub_list)] = [
                        miktar, eleman, price]
    for temp_child in temp:  # leaves have been added to one level above
        helper_tree_maker1(temp_child[0], temp_child[1], listem)

    def is_all_list(liste_parametresi):  # checks all and return False if there is tuple
        for sub_list in liste_parametresi:
            if type(sub_list) == tuple:
                return False
            else:
                if type(sub_list) == list and is_all_list(sub_list) == False:
                    return False
        return True

    def helper_tree_maker2(liste_parametresi):  # generates rest of the tree
        temp = []
        i = 0
        while i < len(liste_parametresi):
            if is_all_list(liste_parametresi[i]):
                temp.append(liste_parametresi[i])
                liste_parametresi.pop(i)
            else:
                i += 1
        for sub_list in temp:
            for kalanlar in liste_parametresi:
                for sub_kalanlar in kalanlar:
                    if type(sub_kalanlar) == tuple and sub_kalanlar[1] == sub_list[0]:
                        miktar = sub_kalanlar[0]
                        kalanlar[kalanlar.index(sub_kalanlar)] = [
                            miktar, sub_list]

    while len(listem) != 1:
        helper_tree_maker2(listem)
    return listem


def calculate_price(part_list):
    if len(part_list) == 1 and type(part_list[0][1]) == float:
        return part_list[0][1]

    tree = tree_maker(part_list)
    prices = []

    def helper_to_calculate_price(list_of_tree, accumulator):
        for child in list_of_tree:
            if type(child) == list and type(child[-1]) != float:
                if type(child[0]) == int:
                    miktar = child[0]
                    helper_to_calculate_price(child, accumulator*miktar)
                else:
                    helper_to_calculate_price(child, accumulator)
            elif type(child) == list and type(child[-1]) == float:
                prices.append(accumulator*child[-1]*child[0])
    helper_to_calculate_price(tree[0], 1)
    res = 0
    for i in prices:
        res += i
    return res


def required_parts(part_list):
    if len(part_list) == 1 and type(part_list[0][1]) == float:
        return [(1, part_list[0][0])]

    tree = tree_maker(part_list)
    result = []

    def helper_to_required_parts(tree, accumulator):
        for child in tree:
            if type(child) == list and type(child[-1]) != float:
                if type(child[0]) == int:
                    helper_to_required_parts(child, accumulator*child[0])
                elif type(child[0]) != int:
                    helper_to_required_parts(child, accumulator)
            elif type(child) == list and type(child[-1]) == float:
                result.append((accumulator*child[0], child[1]))
    helper_to_required_parts(tree[0], 1)
    return result


def stock_check(part_list, stock_list):
    if len(part_list) == 1 and type(part_list[0][1]) == float:
        a = required_parts(part_list)
        if stock_list != [] and a[0][0]-stock_list[0][0] > 0:
            return [(a[0][0]-stock_list[0][0], part_list[0][1])]
        else:
            return []
    tree = tree_maker(part_list)
    elzemler = required_parts(tree)
    double_check = []
    for i in stock_list:
        double_check.append(i[1])
    result = []
    for sub_elzemler in elzemler:
        for sub_stock_list in stock_list:
            if sub_elzemler[1] == sub_stock_list[1]:
                if sub_elzemler[0]-sub_stock_list[0] > 0:
                    result.append(
                        (sub_elzemler[1], sub_elzemler[0]-sub_stock_list[0]))
        if not sub_elzemler[1] in double_check:
            result.append((sub_elzemler[1], sub_elzemler[0]))

    return result
