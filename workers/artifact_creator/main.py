import logging
import traceback
import os
import shutil
import sys
import config
import tempfile
import subprocess
import boto3
import gzip
import json
from conductor.ConductorWorker import ConductorWorker

logging.basicConfig()
log = logging.getLogger('conductor-workers.create_tenant_artifacts_images')
log.setLevel(logging.INFO)

conf = config.get_config()

BUCKET_NAME = os.getenv("BUCKET")

if not BUCKET_NAME:
    raise SystemExit("please set BUCKET env. variable")

if not os.getenv("AWS_SECRET_ACCESS_KEY") or not os.getenv("AWS_ACCESS_KEY_ID"):
    raise SystemExit("please set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID env. variable")

AWS_URL = "https://%s.s3.amazonaws.com" % BUCKET_NAME

RPI3_IMAGES = {"RPI3_SDIMG": "rpi3/%s/mender-raspberrypi3_%s.sdimg" % (conf.rpi_version, conf.rpi_version),
               "RPI3_RELEASE_1": "rpi3/%s/raspberrypi3_release_1_%s.mender" % (conf.rpi_version, conf.rpi_version),
               "RPI3_RELEASE_2": "rpi3/%s/raspberrypi3_release_2_%s.mender" % (conf.rpi_version, conf.rpi_version)}

BBB_IMAGES = {"BBB_SDIMG": "bbb/%s/mender-beaglebone_%s.sdimg" % (conf.bbb_version, conf.bbb_version),
              "BBB_RELEASE_1": "bbb/%s/beaglebone_release_1_%s.mender" % (conf.bbb_version, conf.bbb_version),
              "BBB_RELEASE_2": "bbb/%s/beaglebone_release_2_%s.mender" % (conf.bbb_version, conf.bbb_version)}

VEXPRESS_IMAGES = {"VEXPRESS_RELEASE_1": "vexpress-qemu/%s/vexpress_release_1_%s.mender" % (conf.vexpress_version, conf.vexpress_version),  
                   "VEXPRESS_RELEASE_2": "vexpress-qemu/%s/vexpress_release_2_%s.mender"  % (conf.vexpress_version, conf.vexpress_version)}

BACKEND_HOST = "https://hosted.mender.io"
s3 = boto3.resource('s3')

def check_config():
    golden_image = "images"

    # make sure image versions exist in container 
    if conf.rpi_version:
        for image_type, image_file in RPI3_IMAGES.items():
            assert os.path.exists(os.path.join(golden_image, image_file))
        log.info("found rpi3 images for version %s", conf.rpi_version)

    if conf.bbb_version:
        for image_type, image_file in BBB_IMAGES.items():
            assert os.path.exists(os.path.join(golden_image, image_file))
        log.info("found bbb images for version %s", conf.bbb_version)

    if conf.vexpress_version:
        for image_type, image_file in VEXPRESS_IMAGES.items():
            assert os.path.exists(os.path.join(golden_image, image_file))
        log.info("found vexpress-qemu images for version %s", conf.vexpress_version)

    assert os.path.exists("mender-artifact")


def gzip_file(f):
    with open(f, 'rb') as f_in, gzip.open(f + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    return f + '.gz'

def upload_s3(key, f):
    log.info("uploading file %s to object key %s" % (f, key))

    data = open(f, 'rb')
    s3.Bucket(BUCKET_NAME).put_object(Key=key, Body=data, ACL='public-read')

def create_artifacts(task):
    tenant_id = task["inputData"]["tenant_id"]
    tenant_token = task["inputData"]["tenant_token"]

    log.info("starting job for tenant: %s, with tenant_token: %s" % (tenant_id, tenant_token))

    # get temp directory, without actually creating one (else copytree will fail)
    tempfolder = "images_" + next(tempfile._get_candidate_names())
    shutil.copytree("images", tempfolder)
    artifacts = {"links": {}}

    try:
        if conf.bbb_version:
            for image_type, image_file in BBB_IMAGES.items():
                new_image_file = os.path.join(tempfolder, image_file)
                subprocess.check_output("./mender-artifact modify %s --server-uri '%s' -t '%s'" % (new_image_file, BACKEND_HOST, tenant_token), shell=True)

                if new_image_file.endswith(".sdimg"):
                    new_image_file = gzip_file(new_image_file)

                new_image_filename = os.path.basename(new_image_file)
                upload_s3("%s/%s" % (tenant_id, new_image_filename), new_image_file)

                artifacts["links"].setdefault("beaglebone", {}).setdefault(conf.bbb_version, {})
                artifacts["links"]["beaglebone"][conf.bbb_version][new_image_filename] = "%s/%s/%s" % (AWS_URL, tenant_id, new_image_filename)

        if conf.rpi_version:
            for image_type, image_file in RPI3_IMAGES.items():
                new_image_file = os.path.join(tempfolder, image_file)
                subprocess.check_output("./mender-artifact modify %s --server-uri '%s' -t '%s'" % (new_image_file, BACKEND_HOST, tenant_token), shell=True)

                if new_image_file.endswith(".sdimg"):
                    new_image_file = gzip_file(new_image_file)

                new_image_filename = os.path.basename(new_image_file)
                upload_s3("%s/%s" % (tenant_id, os.path.basename(new_image_file)), new_image_file)

                artifacts["links"].setdefault("raspberrypi3", {}).setdefault(conf.rpi_version, {})
                artifacts["links"]["raspberrypi3"][conf.rpi_version][new_image_filename] = "%s/%s/%s" % (AWS_URL, tenant_id, new_image_filename)

        if conf.vexpress_version:
            for image_type, image_file in VEXPRESS_IMAGES.items():
                new_image_file = os.path.join(tempfolder, image_file)
                subprocess.check_output("./mender-artifact modify %s --server-uri '%s' -t '%s'" % (new_image_file, BACKEND_HOST, tenant_token), shell=True)

                if new_image_file.endswith(".sdimg"):
                    new_image_file = gzip_file(new_image_file)

                new_image_filename = os.path.basename(new_image_file)
                upload_s3("%s/%s" % (tenant_id, os.path.basename(new_image_file)), new_image_file)

                artifacts["links"].setdefault("vexpress", {}).setdefault(conf.vexpress_version, {})
                artifacts["links"]["vexpress"][conf.vexpress_version][new_image_filename] = "%s/%s/%s" % (AWS_URL, tenant_id, new_image_filename)



        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(json.dumps(artifacts))
        
        upload_s3("%s/%s" % (tenant_id, "links.json"), tmp.name)

        # always return this well formed response - status, output, logs
        return {'status': 'COMPLETED',
                'output': { "artifacts": artifacts},
                'logs': []}
    except:
        err = str(traceback.format_exc())
        log.warn("failed: " + str(err))

        return {'status': 'FAILED',
                'output': err,
                'logs': []}
    
    # cleanup temp folder
    finally:
        shutil.rmtree(tempfolder)

def main():
    log.info('create_tenant'.format(conf.conductor))
    cc = ConductorWorker(conf.conductor + "/api", 1, 0.1)

    check_config()
    cc.start('create_tenant', create_artifacts, True)
    

if __name__ == '__main__':
    main()
