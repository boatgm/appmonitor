#!/bin/bash
#========================================================================
#   FileName: apksdk.sh
#     Author: gongming
#      Email: mg90@foxmail.com
#   HomePage: wrud.net
# LastChange: 2013-01-18 22:08:20
#========================================================================
path_apktool="./"
path_apk_store="./"
path_apktooled="./"
path_jad="./"

wget "http://" temp

filename = `md5sum temp`
mv temp $filename
apktool d temp filename
grep -PhR "sdk"


sudo $path_apktool d $path_apk_store $path_apktooled

regurl = v.replace('*','[\w]*')
grepcmd = 'sudo grep -P -h -R "' + regurl + '" '

+ self.get_apk_apktooled_path(apk_name,market,cg)
data=subprocess.Popen(grepcmd,stdout=subprocess.PIPE,shell=True)
result =  (data.stdout.read())
sudo rm -r _apk_apktooled_path
sudo rm -r _apk_store_path(apk_name,market,cg))

sudo grep -P -h -R "regurl" _apktooled_path/apk_name

if not os.path.exists(temp[0]+'/src'):
#unjar jar -xvf test.jar -C classes
sudo unzip jarFile -d temp[0]/classes

#jad -r -ff -d src -s java classes/**/*.classes
sudo jadpath jad -r -ff -d temp[0]/src -s java temp[0]/classes/**/*.class"
