# 用于CDN刷新节点上的文件内容，参数依次为：AK,SK,PATH,TYPE
# 详见接口文档：https://help.aliyun.com/document_detail/91164.html
import sys
import os
import logging
from typing import List
import urllib.parse
from Tea.core import TeaCore

from alibabacloud_cdn20180510.client import Client as Cdn20180510Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cdn20180510 import models as cdn_20180510_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient


class DirFlush:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Cdn20180510Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'cdn.aliyuncs.com'
        return Cdn20180510Client(config)

    @staticmethod
    def main(
            access_key_id: str,
            access_key_secret: str,
            object_path: str,
            object_type: str = 'File',
    ):
        """
        刷新/预热CDN方法
        :param access_key_id: ak 必填
        :param access_key_secret: sk 必填
        :param object_path: 目录，多个目录之间使用换行符分割 必填
        :param object_type: 刷新类型。取值：File：文件。 Directory：目录。
        :return:
        """
        client = DirFlush.create_client(access_key_id, access_key_secret)
        refresh_object_caches_request = cdn_20180510_models.RefreshObjectCachesRequest(
            object_path=object_path,
            object_type=object_type
        )
        resp = client.refresh_object_caches(refresh_object_caches_request)
        resp_str = UtilClient.to_jsonstring(TeaCore.to_map(resp))
        ConsoleClient.log(resp_str)
        return resp_str

    @staticmethod
    async def main_async(
            access_key_id: str,
            access_key_secret: str,
            object_path: str,
            object_type: str = 'File',
    ) -> None:
        """
        刷新/预热CDN方法（异步）
        :param access_key_id: ak 必填
        :param access_key_secret: sk 必填
        :param object_path: 目录，多个目录之间使用换行符分割 必填
        :param object_type: 刷新类型。取值：File：文件。 Directory：目录。
        :return:
        """
        client = DirFlush.create_client(access_key_id, access_key_secret)
        refresh_object_caches_request = cdn_20180510_models.RefreshObjectCachesRequest(
            object_path=object_path,
            object_type=object_type
        )
        resp = await client.refresh_object_caches_async(refresh_object_caches_request)
        ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))


HELLO_WORLD = b'Hello world!\n'


# To enable the initializer feature (https://help.aliyun.com/document_detail/158208.html)
# please implement the initializer function as below：
# def initializer(context):
#    logger = logging.getLogger()
#    logger.info('initializing')


def handler(environ, start_response):
    """
    Web调用入口
    遵循WSGI规范
    用于阿里云FC函数调用功能调用
    通过Get请求的requestParam分别写入如下参数
    path（刷新目录，如：http://www.baidu.com/)
    type（刷新类型，枚举：File：文件  Directory：目录。）
    :param environ: 通过requestParam分别写入path（刷新目录)
    :param start_response:
    :return: 返回执行结果
    """
    # context = environ['fc.context']
    # request_uri = environ['fc.request_uri']
    for k, v in environ.items():
        if k.startswith('HTTP_'):
            # process custom request headers
            pass
    # do something here
    request_param = urllib.parse.parse_qs(environ['QUERY_STRING'])
    ak = os.getenv("CDN_AK")
    sk = os.getenv("CDN_SK")
    path = request_param["path"][0]
    object_type = request_param["type"][0]
    object_type = "File" if (
            object_type is None
            or
            (object_type != "Directory" and object_type != "File")
    ) \
        else object_type  # 用来为object_type赋予一个默认值
    try:
        result = DirFlush.main(ak, sk, path, object_type)
    except IOError as err:
        logging.log(err)
        raise err
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [result.encode()]


if __name__ == '__main__':
    """
    主程序入口
    """
    if len(sys.argv[1:]) < 4:
        DirFlush.main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        DirFlush.main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
