
# Handson2: tcache poisoning(double-free)をやる. 
単純に0xdeadbeefで書き換えるだけ.  SIGSEGVで落ちるまで, 任意書き込み. 
```python
create_note()
delete_note()
delete_note()
create_note()
create_note()
``` 
