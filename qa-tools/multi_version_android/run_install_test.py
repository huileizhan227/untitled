import sys
import pytest

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('arg1: old apk path; arg2: new apk path')
        sys.exit(0)
    old = sys.argv[1]
    new = sys.argv[2]
    pytest.main(args=[
        '-s',
        '--apk-old={}'.format(old),
        '--apk-new={}'.format(new),
        'multi_version_android/install_test.py',
    ])
