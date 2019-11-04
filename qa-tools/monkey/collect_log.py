import os
import sys

from monkey_auto import crash_collection

def main(log_folder):
    crash_file = os.path.join(log_folder, 'crash.log')
    anr_folder = os.path.join(log_folder, 'anr')
    if not os.path.exists(anr_folder):
        os.makedirs(anr_folder)


    crash_collection.to_file(log_folder, crash_file)
    crash_collection.collect_anr(log_folder, anr_folder)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('log folder?')
        os.system('pause')
        sys.exit()

    log_folder = sys.argv[1]
    main(log_folder)
