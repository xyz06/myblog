from qiniu import Auth, put_file, etag,put_data,BucketManager
import qiniu.config

def upload_qn(filestroge):

    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'vEDMkIFJWPFSgcRlBDbm-vdCGV_uzlVTtie_ZV-4'
    secret_key = 'Lv_xIg3Z-PpqXE9DnR6-qLpS4oSOp_zEBoTjIz24'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'Bucket_Name'
    # 上传后保存的文件名
    # key = 'my-python-logo.png'
    filename = filestroge.filename
    suffix = filename.rsplit('.')[-1]
    ran = random.randit(1,1000)
    key = filename.rsplit('.')[0] + '_' + str(ran) + '.' + suffix
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, filestroge.read())


    return info,ret



def delete_qn(key):

    access_key = 'vEDMkIFJWPFSgcRlBDbm-vdCGV_uzlVTtie_ZV-4'
    secret_key = 'Lv_xIg3Z-PpqXE9DnR6-qLpS4oSOp_zEBoTjIz24'

    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = 'Bucket_Name'
    key = 'python-logo.png'
    # 删除bucket_name 中的文件 key
    ret, info = bucket.delete(bucket_name, key)
    # print(info)
    # assert ret == {}
    return info