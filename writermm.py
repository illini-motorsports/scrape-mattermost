from postmm import MMPost


def write_to_file(filename: str, posts: list[MMPost]) -> None:
    with open(filename, "w") as FILE:
        for post in posts[::-1]:
            FILE.write(str(post))
            FILE.write("---------------------------------\n")