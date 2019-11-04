# more jenkins

jenkins for More

## install

```python
python setup.py install
```

## usage

### get last build info

```python
from more_jenkins import master

master.request() # init before get info
build_id = master.build_id
project_name = master.project_name
is_stable = master.is_stable
if is_stable:
    apk_link = master.get_apk_link()
    all_apk_links = test.get_all_apk_links()
```

### get other project info

```python
import more_jenkins
coco = more_jenkins.Jenkins(
    rss_url='https://package.more.buzz/job/transsnet_coco/rssAll'
)
coco.request()
coco.build_id
```

### customize apk download link finder

```python
from more_jenkins import Jenkins

test = Jenkins(
    rss_url='https://package.more.buzz/job/Test/rssAll',
    apk_link_pattern_list=[
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+normal[^\s\'\"]+\.apk(?=[\'\"])',
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+common[^\s\'\"]+\.apk(?=[\'\"])',
        '(?<=href=[\'\"])[mM]ore[^\s\'\"]+\.apk(?=[\'\"])'
    ]
)
apk_link = test.get_apk_link()
all_apk_links = test.get_all_apk_links()
```

`get_all_apk_links` will use the last pattern in `apk_link_pattern_list`.

`get_apk_link` will use the patterns in order, until finding a link.
