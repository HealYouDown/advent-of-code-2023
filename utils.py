def get_input(day: int) -> str:
    with open(f"./inputs/{str(day).rjust(2, '0')}.txt", "r") as fp:
        return fp.read()
