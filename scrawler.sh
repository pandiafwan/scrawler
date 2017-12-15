#!/bin/bash

ROOT_DIR=`dirname $0`
SCRIPT_NAME=`basename $0`
if [ "${ROOT_DIR}" == "." ]
then
	echo "Please use fullpath, eg./your/path/$0"
	exit 100
fi

if [ $# -lt 2 ]
then
	echo "Please give <crawlid> <url>"
	exit 200
fi

CRAWL_ID=$1
URL=$2

LOCK_FILE=${ROOT_DIR}/crawling_runner_${CRAWL_ID}.lck
if [ -e ${LOCK_FILE} ]
then
	echo "[INFO] `date +"%Y-%m-%d %H:%M:%S"` - Another process is still running"
	exit 0
fi

touch ${LOCK_FILE}

echo "[INFO] `date +"%Y-%m-%d %H:%M:%S"` - Start crawling"

cd ${ROOT_DIR}

echo "[INFO] `date +"%Y-%m-%d %H:%M:%S"` - Running spider url : ${URL}"
scrapy crawl inject -a url=${URL} -a crawlid=${CRAWL_ID}

rm -f ${LOCK_FILE}
echo "[INFO] `date +"%Y-%m-%d %H:%M:%S"` - Finished crawling"