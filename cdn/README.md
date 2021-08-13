# CDN操作脚本

## 使用方式
每个脚本给出2个调用方式：
- __main__函数调用：用于从当前类启动时，通过命令行进行调用
- 遵循WSGI规范的handler方法调用，用于Web请求类或者阿里云FC的Web触发使用

## dir_flush.py

- [刷新节点上的文件内容](https://help.aliyun.com/document_detail/91164.html)
- 运行参数依次为
    - AK
    - SK
    - PATH
    - TYPE(非必填)