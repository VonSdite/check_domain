# check_domain
穷举哪些域名未被购买

## 快速使用
修改配置文件`config.ini`
```
[query]
dict = 'abcdefghijklmnopqrstuvwxyz0123456789'
base_domain = '.ai'
len_start = 1
len_end = 6
```

- `dict`是要穷举的字符字典, 比如设置`dict='ab'`, 穷举长度为2的域名就会是 aa、ab、ba、bb四种情况
- `base_domain`是域名后缀, 比如`base_domain=.com`, 就会查询类似a.com、b.com的域名
- `len_start`域名长度的起始值, 设为1, 表明穷举从长度为1开始
- `len_end`域名长度的终止值, 设为6, 表明穷举的最大长度域名为6个字符

**未被购买的域名**, 会保存在`save.txt`中
