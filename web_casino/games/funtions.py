def split(crd_1, crd_2, crd_d):
    dict_split = {'22': '2345678', '33': '2345678', '44': '56', '55': '',
                  '66': '23456', '77': '234567', '88': '23456789', '99': '2345689',
                  '1010': '', 'AceAce': '2345678910'}
    if crd_1 == crd_2 and crd_d in dict_split[crd_1 + crd_2]:
        return 'Split'
    else:
        return 'None'


def bj_count(crd_1, crd_2, crd_d):

    def double(crd_1, crd_2, crd_d):
        dict_double = {'2Ace': '56', 'Ace2': '56', '3Ace': '56', 'Ace3': '56', '4Ace': '456',
                       'Ace4': '456', '5Ace': '456', 'Ace5': '456', '6Ace': '3456',
                       'Ace6': '3456', '7Ace': '3456', 'Ace7': '3456', 'Ace8': '',
                       '8Ace': '', 'Ace9': '', '9Ace': '', '10Ace': '', 'Ace10': '', 'AceAce': ''}

        dict_double_strong = {'9': '3456', '10': '23456789', '11': '23456789'}

        if crd_1 == 'Ace' or crd_2 == 'Ace':
            if crd_d in dict_double[crd_1 + crd_2]:
                return 'Double'
        elif 8 < int(crd_1) + int(crd_2) < 12:
            if crd_d in dict_double_strong[str(int(crd_1) + int(crd_2))]:
                return 'Double'

        return 'None'

    def hit(crd_1, crd_2, crd_d):
        dict_card = {'2': '13', '3': '13', '4': '12', '5': '12', '6': '12', '7': '17',
                     '8': '17', '9': '17', '10': '17', '1': '17'}
        if int(crd_1) + int(crd_2) < int(dict_card[crd_d]):
            return 'Hit'
        else:
            return 'None'

    result = 'Stand'
    crd = [crd_1, crd_2, crd_d]
    crda = [crd_1, crd_2, crd_d]
    for i in range(3):
        if crd[i] in 'JackQueenKing':
            crd[i] = '10'
        if crda[i] == 'Ace':
            crda[i] = '1'
        if crda[i] in 'JackQueenKing':
            crda[i] = '10'
    results = [split(crd[0], crd[1], crd[2]), double(crd[0], crd[1], crd[2]),
               hit(crda[0], crda[1], crda[2])]
    for i in results:
        if i == 'None':
            continue
        else:
            result = i
            break

    return result


def get_statistic(hands, wins):
    return wins / hands - 0.487
