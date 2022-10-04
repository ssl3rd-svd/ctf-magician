# CTF Magician

## Project structure

```plain-text
PROJECT
- database
- config
- challenges
    - challenge_1
        - files
            - file_a
            - file_b
            - file_c
            ...
        - urls
            - url_a
            - url_b
            - url_c
            ...
    - challenge_2
        - sockets
            - sock_a
            - sock_b
            - sock_c
            ...
        - sshs
            - ssh_a
            - ssh_b
            - ssh_c
            ...
    - challenge_*
    ...
- reports
    - report_1
    - report_2
    - report_*
```

## Plugin structure

```plain-text
- plugin
    - feeder
        - ctfd_feeder
    - scanner
        - initial_scanner
        - file_structure_scanner
        - vulnerability_scanner
        - ...
    - extractor
        - archive_extractor
            - zip_extractor
            - tar_extractor
            - cpio_extractor
            ...
        - file_system_extractor
            - ext_extractor
            - fat32_extractor
            ...
    - fuzzer
        ...
```

## Interfaces

```plain-text
- interfaces
    - CLI
    - HTTP/Web
    - Qt5
```
