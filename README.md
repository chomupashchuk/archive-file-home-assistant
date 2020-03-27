# Archive files in Home Assistant
Archive file service for Home Assistant. For example archive snapshots.


## Integration installation
In `/config` folder create `custom_components` folder and load source files folder `archive` in it. In 'configuration.yaml' include:
```
archive:
```

## Services
### Service: archive.file
`archive.file` is used to delete a file.

#### attributes:
- `file` is used to indicate file path. it is a mandatory attribute.
- `target` is folder to store the archive in. It is an optional attribute.
- `name` is the name of the archive (`.zip` to be added automatically). Default name is an UTC time. It is an optional attribute.

#### Example 1
```
service: archive.file
data:
  file: '/config/image_snapshot/photo.png'
```

#### Example 2
```
service: archive.file
data:
  file: '/config/image_snapshot/photo.png'
  target: '/config/old_snapshots/'
  name: 'latest_snapshots'
```

### Service: archive.files_in_folder
`archive.files_in_folder` is used to archive files within the folder, where files shall be archive if they are older than specified period of time in seconds (default is 24 hours).

#### attributes:
- `folder` is used to indicate folder path. it is a mandatory attribute.
- `time` is used to indicate how old files must be  in seconds in order to be archived. Default is 24 hours (86400 seconds). It is an optional attribute.
- `only_extensions` is list of extensions of files that are allowed to be archived. Cannot be used together with `except_extensions`. It is an optional attribute.
- `except_extensions` is list of extensions of files that are not allowed to be archived. Cannot be used together with `only_extensions`. It is an optional attribute.
- `target` is folder to store the archive in. It is an optional attribute.
- `name` is the name of the archive (`.zip` to be added automatically). Default name is an UTC time. It is an optional attribute.

#### Example 1
```
service: archive.files_in_folder
data:
  folder: '/config/image_snapshot/'
  time: 604800
```

#### Example 2
```
service: archive.files_in_folder
data:
  folder: '/config/image_snapshot/'
  target: '/config/old_snapshots/'
  only_extensions:
    - '.png'
    - '.jpg'
```

#### Example 3
```
service: archive.files_in_folder
data:
  folder: '/config/image_snapshot/'
  time: 24000
  except_extensions:
    - '.zip'
    - '.yaml'
```
