import sqlite3
from logging import getLogger, config
from dict_config import dict_config
import re

config.dictConfig(dict_config)
logger = getLogger("logger")

NEGATIVES_DICT = dict()


def find_indexes(pattern: str):
    logger.debug(f"func called: find_indexes( {pattern} )")
    stack = []
    for index, char in enumerate(pattern):
        if char == "(":
            stack.append(index)
        elif char == ")":
            if stack:
                ob_ind = stack.pop()
                logger.debug(f"func returns:  ob_ind, index: {[ob_ind, index]}")
                return ob_ind, index
            else:
                raise ValueError("Too many closed brackets")


def replace_negative(negative_n: int) -> str:
    logger.debug(f"func called: replace_negative( {negative_n} )")
    if NEGATIVES_DICT:
        last_key_num: int = int(
            list(
                NEGATIVES_DICT.keys()
            )[-1][1:-1]
        )
        new_key = "n" + str(last_key_num+1) + "n"
        NEGATIVES_DICT[new_key] = negative_n
        logger.debug(f"func returns: new_key: {new_key}")
        return new_key
    else:
        NEGATIVES_DICT["n0n"] = negative_n
        logger.debug("func returns: n0n")
        return "n0n"


def parce_and_replace_negative(equation: str):
    logger.debug(f"func called: parce_and_replace_negative( {equation} )")
    matches = re.findall(r"\(-\d+\)", equation)
    for neg_n in matches:
        neg_n_key = replace_negative(float(neg_n[1:-1]))
        equation = equation.replace(neg_n, neg_n_key)
    logger.debug(f"func returns: equation: {equation}")
    return equation


def do_powers(equation: str):
    logger.debug(f"func called: do_powers( {equation} )")
    matches = re.findall(r"(n?\d+\.?\d*+n?)\^(n?\d+\.?\d*+n?)", equation)
    for power_group in matches:
        num_pow_list = list()
        for num in power_group:
            if num.startswith("n"):
                num_pow_list.append(NEGATIVES_DICT[num])
            else:
                num_pow_list.append(float(num))

        equation = equation.replace(
            "^".join([power_group[0], power_group[1]]),
            (str(num_pow_list[0]**num_pow_list[1]))
        )
    logger.debug(f"func returns: equation: {equation}")
    return equation


def do_multidiv(equation: str) -> str:
    logger.debug(f"func called: do_multidiv( {equation} )")
    while "*" in equation or "/" in equation:
        match = re.search(r"(n?\d+\.?\d*+n?)([*/])(n?\d+\.?\d*+n?)", equation)
        nums_list = list()
        for num in [match.group(1), match.group(3)]:
            if num.startswith("n"):
                nums_list.append(NEGATIVES_DICT[num])
            else:
                nums_list.append(float(num))
        if match.group(2) == "*":
            result = nums_list[0] * nums_list[1]
        else:
            result = nums_list[0] / nums_list[1]

        equation = equation.replace(
            match.group(),
            str(result)
        )
    logger.debug(f"func returns: equation: {equation}")
    return equation


def do_plussub(equation: str) -> int:
    logger.debug(f"func called: do_plussub( {equation} )")
    match: list[str] = re.findall(r"[+-]?n?\d+\.?\d*n?", equation)
    nums = list()
    for elem in match:
        if elem.endswith("n"):
            if elem.startswith("-"):
                nums.append(NEGATIVES_DICT[elem[1:]]*(-1))
            elif elem.startswith('+'):
                nums.append(NEGATIVES_DICT[elem[1:]])
            else:
                nums.append(NEGATIVES_DICT[elem])
        else:
            nums.append(float(elem))
    answer = sum(nums)
    logger.debug(f"func returns: answer: {answer}")
    return answer


def do_math(equation: str):
    logger.debug(f"func called: do_math( {equation} )")
    if "^" in equation:
        equation = do_powers(equation)
    if "*" in equation or "/" in equation:
        equation = do_multidiv(equation)
    if "+" in equation or "-" in equation:
        equation = do_plussub(equation)
    if float(equation) < 0:
        equation = replace_negative(equation)
    logger.debug(f"func returns: equation: {equation}")
    return equation


def return_final_answer(equation: str) -> float:
    logger.debug(f"func called: return_final_answer( {equation} )")
    if str(equation).startswith("n") and str(equation).endswith("n"):
        equation = NEGATIVES_DICT[equation]
    logger.debug(f"func returns: answer: {equation}")
    return float(equation)


def calculator(equation: str):
    # equation: str = input("Type in an equation:\n").replace(" ", "")

    logger.debug("")
    logger.debug("Program started")

    equation = parce_and_replace_negative(equation)
    while True:
        try:
            ob, cb = find_indexes(equation)
            equation = equation.replace(
                equation[ob:cb+1], str(do_math(equation[ob+1:cb]))
            )
        except TypeError:
            logger.info(f"error intercepted: TypeError. Equation: {equation}")
            answer = do_math(equation)
            logger.debug(f"func returns: answer: {answer}")
            return return_final_answer(answer)
        except Exception as e:
            print(f"Error: {e}")
            break
    logger.debug("Program finished")


if __name__ == "__main__":
    print(calculator("3+2"))
