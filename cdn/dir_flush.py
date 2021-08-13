# 用于CDN刷新节点上的文件内容，参数依次为：AK,SK,PATH,TYPE
# 详见接口文档：https://help.aliyun.com/document_detail/91164.html
import sys

from typing import List
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
    ) -> None:
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
        ConsoleClient.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))

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


if __name__ == '__main__':
    if len(sys.argv[1:]) < 4:
        DirFlush.main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        DirFlush.main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
