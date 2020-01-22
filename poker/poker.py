#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

import itertools


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_rank(card):
    letter_rank_description = {
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    r = card[0]
    if r in letter_rank_description:
        return letter_rank_description[r]
    else:
        return int(r)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = [card_rank(x) for x in hand]
    return sorted(ranks, reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    first = hand[0][1]
    result = list(itertools.takewhile(lambda x: x[1] == first, hand))
    return len(result) == len(hand)


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    result = sorted(ranks)
    first = result[0]
    expected = list(map(lambda x: x + first, range(5)))
    return result == expected


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    temp = list(itertools.takewhile(lambda x: ranks.count(x) != n, ranks))
    nothing_found = len(temp) == len(ranks)
    return None if nothing_found else ranks[len(temp)]


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    sorted_r = sorted(ranks, reverse=True)
    temp = [(k, len(list(g))) for k, g in itertools.groupby(sorted_r)]
    if temp[0][1] >= 2 and temp[1][1] >= 2:
        return temp[0][0], temp[1][0]
    return None


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    hands_5 = iter(itertools.combinations(hand, 5))
    best_hand_5 = next(hands_5)
    best_rank = hand_rank(best_hand_5)
    for hand in hands_5:
        rank = hand_rank(hand)
        if best_rank < rank:
            best_rank = rank
            best_hand_5 = hand
    return best_hand_5


def make_one_hand_substitute(index, hand):
    cards = '2 3 4 5 6 7 8 9 T J Q K A'.split()
    possible_values = list()
    result = list()
    if hand[index] == '?R':
        hearts = list(map(lambda x: x + 'H', cards))
        diamonds = list(map(lambda x: x + 'D', cards))
        possible_values = hearts + diamonds

    if hand[index] == '?B':
        clubs = list(map(lambda x: x + 'C', cards))
        spades = list(map(lambda x: x + 'S', cards))
        possible_values = clubs + spades

    for v in possible_values:
        temp_hand = hand.copy()
        if v not in temp_hand:
            temp_hand[index] = v
            result.append(temp_hand)

    return result


def joker_substitute(hand: list):
    no_substitute = list()
    if '?R' not in hand and '?B' not in hand:
        no_substitute.append(hand)
        return no_substitute

    first_substitute = list()
    if '?R' in hand:
        index = hand.index('?R')
        first_substitute = make_one_hand_substitute(index, hand)
    else:
        first_substitute.append(hand)

    second_substitute = list()
    if '?B' in hand:
        index = hand.index('?B')
        for temp_hand in first_substitute:
            temp_substitute = make_one_hand_substitute(index, temp_hand)
            second_substitute += temp_substitute
        return second_substitute
    else:
        return first_substitute


def best_wild_hand(hand):
    """best_hand но с джокерами"""

    hands_7_collection = joker_substitute(hand)
    best_hands_5 = list()
    for hand_7 in hands_7_collection:
        best_hand_5 = best_hand(hand_7)
        best_hand_5_rank = hand_rank(best_hand_5)
        best_hands_5.append((best_hand_5, best_hand_5_rank))

    best_hands_5_sorted = sorted(best_hands_5, key=lambda x: x[1], reverse=True)
    return best_hands_5_sorted[0][0]


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
