import os
import shutil


def recursive_copy(source, destination):
    # delete everything in the destination directory
    if os.path.exists(destination):
        print(f"removed {destination}")
        shutil.rmtree(destination)

    # create directory at destination so that the base case check can happen
    os.mkdir(destination)
    print("made destination")

    # base case: if the source and destination subdirectories are the same, break out
    if os.listdir(destination) == os.listdir(source):
        print("base case reached")
        return

    for subdirectory in os.listdir(source):
        new_source = os.path.join(source, subdirectory)
        new_destination = os.path.join(destination, subdirectory)
        print(f"{new_source} -> {new_destination}")

        if os.path.isfile(new_source):
            shutil.copy(new_source, new_destination)
        else:
            recursive_copy(new_source, new_destination)
