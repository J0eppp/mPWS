# mPWS
Miniprofielwerkstuk van Sam Statijen en Joep van Dijk


# Usage
## Get all the data
```console
foo@bar:~/mPWS/src $ python get_data_from_luchtmeetnet.py
```

## Combine all the files to four big files
```console
foo@bar:~/mPWS/src $ python combine_all_json_files.py ../data ../data_combined
```

## Get all the important data
```console
foo@bar:~/mPWS/src $ python select_important_data.py ../data_combined ../data_selected
```
