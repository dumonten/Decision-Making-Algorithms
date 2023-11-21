import random


def generate_words(number_of_words, word_max_len, alphabet=("a", "b", "c")):
    words = []
    while len(words) < number_of_words:
        cur_len = random.randint(2, word_max_len)
        word = ""
        for _ in range(cur_len):
            word = word + random.choice(alphabet)
        if word not in words:
            words.append(word)
    # сортировка по длине: по убыванию длины
    words.sort(key=lambda x: len(x), reverse=True)
    # потенциальные остатки от длинных слов (может и не надо добавлять)
    potential_residues_to_add = set()
    for word in words:
        if len(word) == len(words[0]):
            potential_residues_to_add.add(word[-2:])
    # действительные остатки для добавления
    residues_to_add = []
    for residue in potential_residues_to_add:
        if not any([word.endswith(residue) for word in words if len(word) != len(words[0])]):
            residues_to_add.append(residue)
    return words, residues_to_add


def get_grammar(words):
    """
    {
    0: [(a, 1), ((b, a), (c, None)]
    }
    """
    grammar = {}

    def correct_states_and_ways(next_unused_state, curr_state, letter):
        index = -1
        try:
            for i, way in enumerate(grammar[curr_state]):
                # если совпали буквы воруем след. состояние
                if way[0] == letter:
                    index = i
                    break
        except KeyError:
            grammar[curr_state] = []
        # состояние ни разу не встречалось
        if index == -1:
            grammar[curr_state].append((letter, next_unused_state))
            curr_state = next_unused_state
            next_unused_state += 1
        else:
            curr_state = grammar[curr_state][index][1]
        return next_unused_state, curr_state

    # создание правил
    def _1_stage():
        word_max_len = len(words[0])
        # стартовое 0, след. 1
        next_state = 1
        for word in words:
            curr_state = 0
            next_state, curr_state = correct_states_and_ways(next_state, curr_state, word[0])
            if len(word) == word_max_len:
                for letter in word[1:-2]:
                    next_state, curr_state = correct_states_and_ways(next_state, curr_state, letter)
                """
                Пример, когда могут повторяться остатки по две буквы: 
                [abba, abcc]
                abba
                S->aA1
                A1->bA2
                A2-> ba
            
                abcc
                A2->cc
                """
                try:
                    grammar[curr_state].append((word[-2], word[-1]))
                except KeyError:
                    grammar[curr_state] = [(word[-2], word[-1])]
            else:
                for letter in word[1:-1]:
                    next_state, curr_state = correct_states_and_ways(next_state, curr_state, letter)
                try:
                    grammar[curr_state].append((word[-1], None))
                except KeyError:
                    grammar[curr_state] = [(word[-1], None)]

    # убрать все виды ways, как: (b, a)
    def _2_stage():
        # replace what and ON what
        replacement = dict()
        for state, ways in grammar.items():
            replacement_found = False
            for way in ways:
                # если есть сочетание ab
                if type(way[1]) == str and not replacement_found:
                    # второй цикл
                    for second_state, second_ways in grammar.items():
                        # чтобы не было повторений
                        if state == second_state:
                            continue
                        elif replacement_found:
                            break
                        else:
                            # ищем состояние (замену)
                            for second_way in second_ways:
                                if replacement_found:
                                    break
                                # нашли потенциальную замену
                                # ищем глубже
                                if way[0] == second_way[0] and type(second_way[1]) == int:
                                    third_ways = grammar[second_way[1]]
                                    for third_way in third_ways:
                                        if third_way[0] == way[1] and third_way[1] is None:
                                            replacement[state] = second_state
                                            replacement_found = True
                                            break
        # есть минус: происходит удаление всех
        # правил, связанных с заменяемым состоянием
        for key in replacement.keys():
            del grammar[key]

        for key, value in replacement.items():
            for grammar_key in grammar.keys():
                for index, way in enumerate(grammar[grammar_key]):
                    if way[1] == key:
                        # осуществляем замену, где был прежний state
                        grammar[grammar_key][index] = (way[0], value)

    # экивалентность
    def _3_stage():
        """
        Правило эквивалентности:

        Для нетерминалов А и В:

        Выполнены все условия из списка:
        1) Если у А есть раскрытие в терминалы, то у В оно тоже  есть (пример: A->f, B->f)
        2) Если у А есть раскрытие с нетерминалом C, отличным от А и В, то у В оно тоже есть (пример: A->gT, B->gT)
        **3) Если у А есть раскрытие с нетерминалом А или В, то у В есть такое же с нетерминалом А или В (пример: A->yB,
        B->yB; A->cB, B->cA; A->hA, B->hA)
        """
        searching = True
        while searching:
            found = False
            found_states = None
            for first_state in grammar.keys():
                for second_state in grammar.keys():
                    # сразу допускается равенство
                    equiv_flag = True
                    if first_state <= second_state:
                        continue
                    for way in grammar[first_state]:
                        # если терминальное раскрытие
                        if way[1] is None:
                            equiv_flag &= (way[0], None) in grammar[second_state]
                        # если состояние != A и != В
                        if way[1] not in (first_state, second_state):
                            equiv_flag &= (way[0], way[1]) in grammar[second_state]
                        # если состояние = A или = В
                        if way[1] in (first_state, second_state):
                            # разные комбинации
                            equiv_flag &= (way[0], first_state) in grammar[second_state] \
                                       or (way[0], second_state) in grammar[second_state]
                    if equiv_flag:
                        found = True
                        found_states = (second_state, first_state)
                        break
                if found:
                    break
            if found:
                # удаляем одно из состояний A или B
                del grammar[found_states[1]]
                # переписываем упоминания удаленного на оставшийся: склейка
                for grammar_key in grammar.keys():
                    for index, way in enumerate(grammar[grammar_key]):
                        if way[1] == found_states[1]:
                            grammar[grammar_key][index] = (way[0], found_states[0])
            # как только found = true больше не появляется, то выкид
            else:
                searching = False

    _1_stage()
    _2_stage()
    _3_stage()
    return grammar


def generate_word(grammar):
    word = ""
    # start state - S
    curr_state = 0
    while type(curr_state) == int:
        # выбрали tuple
        choice = random.choice(grammar[curr_state])
        # буква
        word = word + choice[0]
        if type(choice[1]) == str:
            word = word + choice[1]
        curr_state = choice[1]
    return word


def words_to_string(words):
    return "\n".join(words)


def grammar_to_string(grammar):
    output = []
    for state, ways in grammar.items():
        state_pointer = None
        if state == 0:
            state_pointer = "S -> "
        else:
            state_pointer = f"A{state} -> "
        # 0: [('a', 1), ('b', 'c'), ('a', None)]
        for way in ways:
            letter = way[0]
            if type(way[1]) == int:
                if way[1] == 0:
                    letter = letter + "S"
                else:
                    letter = letter + f"A{way[1]}"
            if type(way[1]) == str:
                letter = letter + way[1]
            output.append(state_pointer + letter)
    return "\n".join(output)


def generate_example_words(grammar, number_of_words):
    words = []
    for _ in range(number_of_words):
        words.append(generate_word(grammar))
    return words_to_string(words)
