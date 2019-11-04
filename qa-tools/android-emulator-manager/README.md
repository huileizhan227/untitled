# Android Emulator Manager

Manage official android emulator on Windows.

## setup

```python
python setup.py install
```

## emulator manager usage

```python
import android_emulator_manager

# run the emulator
android_emulator_manager.run('pixel2', port=5554)

# stop the emulator
android_emulator_manager.stop('emulator-5554')
```

## emulator pool usage

Configure the `emulators.yml` and add it to environment variable: `EMULATOR_POOL_CONFIG`.

```python
from android_emulator_manager import emulator_pool

# get a device that is not in use
device = emulator_pool.get_one()

# get all the devices not in use
all_device = emulator_pool.get_all()
```
