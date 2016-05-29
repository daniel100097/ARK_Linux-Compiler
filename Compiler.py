import base64
import os
import shutil
import struct
import sys
import time

import zlib


class Compiler:
    @staticmethod
    def str_to_l(st):
        return struct.unpack('q', st)[0]

    def z_unpack(self, src, dst):
        with open(src, 'rb') as f_src:
            try:
                os.makedirs(dst.replace(src.split("/")[-1:][0], ""))
            except:
                pass

            with open(dst[:-2], 'wb') as f_dst:
                f_src.read(8)
                size1 = self.str_to_l(f_src.read(8))
                f_src.read(8)
                size2 = self.str_to_l(f_src.read(8))
                if (size1 == -1641380927):
                    size1 = 131072L
                runs = (size2 + size1 - 1L) / size1
                array = []
                for i in range(runs):
                    array.append(f_src.read(8))
                    f_src.read(8)
                for i in range(runs):
                    to_read = array[i]
                    compressed = f_src.read(self.str_to_l(to_read))
                    decompressed = zlib.decompress(compressed)
                    f_dst.write(decompressed)

    def __init__(self, src_file, des_file):
        self.z_unpack(src_file, des_file)


class Main:
    def __init__(self, src_dir, des_dir, mod_id):
        if self.make(src_dir, des_dir):
            if self.mod_file(src_dir, des_dir, mod_id):
                print "UPDATE Successfully " + mod_id

    @staticmethod
    def make(src_dir, des_dir):
        files = os.popen("find " + src_dir + "/WindowsNoEditor/" + " -name *.z").read().split("\n")
        for File in files:
            if len(File) > 1:
                Compiler(File, File.replace("/WindowsNoEditor", "").replace(src_dir, des_dir))
        try:
            shutil.copy(src_dir + "/WindowsNoEditor/modmeta.info", des_dir + "/modmeta.info")
            shutil.copy(src_dir + "/WindowsNoEditor/mod.info", des_dir + "/mod.info")
        except:
            pass
        return True

    @staticmethod
    def mod_file(src_dir, des_dir, mod_id):
        shell_file = base64.b64decode(
            "IyEvdXNyL2Jpbi9lbnYgYmFzaAptb2RkZXN0ZGlyPSI0NTEyNTQ1NDEyMTI1Igptb2RpZD01MDUxNDE1NDU0NQoKICAgIHBlcmwgLWUgJwogICAgICBteSAkZGF0YTsKICAgICAgeyBsb2NhbCAkLzsgJGRhdGEgPSA8U1RESU4+OyB9CiAgICAgIG15ICRtYXBuYW1lbGVuID0gdW5wYWNrKCJAMCBMPCIsICRkYXRhKTsKICAgICAgbXkgJG1hcG5hbWUgPSBzdWJzdHIoJGRhdGEsIDQsICRtYXBuYW1lbGVuIC0gMSk7CiAgICAgICRtYXBuYW1lbGVuICs9IDQ7CiAgICAgIG15ICRtYXBmaWxlbGVuID0gdW5wYWNrKCJAIiAuICgkbWFwbmFtZWxlbiArIDQpIC4gIiBMPCIsICRkYXRhKTsKICAgICAgbXkgJG1hcGZpbGUgPSBzdWJzdHIoJGRhdGEsICRtYXBuYW1lbGVuICsgOCwgJG1hcGZpbGVsZW4pOwogICAgICBwcmludCBwYWNrKCJMPCBMPCBMPCBaOCBMPCBDIEw8IEw8IiwgJEFSR1ZbMF0sIDAsIDgsICJNb2ROYW1lIiwgMSwgMCwgMSwgJG1hcGZpbGVsZW4pOwogICAgICBwcmludCAkbWFwZmlsZTsKICAgICAgcHJpbnQgIlx4MzNceEZGXHgyMlx4RkZceDAyXHgwMFx4MDBceDAwXHgwMSI7CiAgICAnICRtb2RpZCA8IiRtb2RkZXN0ZGlyL21vZC5pbmZvIiA+IiRtb2RkZXN0ZGlyLy5tb2QiCiAgICBpZiBbIC1mICIkbW9kZGVzdGRpci9tb2RtZXRhLmluZm8iIF07IHRoZW4KICAgICAgY2F0ICIkbW9kZGVzdGRpci9tb2RtZXRhLmluZm8iID4+IiRtb2RkZXN0ZGlyLy5tb2QiCiAgICBlbHNlCiAgICAgIGVjaG8gLW5lICdceDAxXHgwMFx4MDBceDAwXHgwOFx4MDBceDAwXHgwME1vZFR5cGVceDAwXHgwMlx4MDBceDAwXHgwMDFceDAwJyA+PiIkbW9kZGVzdGRpci8ubW9kIgoJICBlY2hvIGNhdCAiJG1vZGRlc3RkaXIvLm1vZCIKICAgIGZpCiAgICBlY2hvICIkbW9kYnJhbmNoIiA+IiRtb2RkZXN0ZGlyLy5tb2RicmFuY2giCg==").replace(
            "4512545412125", des_dir).replace("50514154545", mod_id)
        open(src_dir + "/Mod.sh", "w").write(shell_file)
        print "Make {0} mod".format(mod_id)
        os.popen("bash " + src_dir + "/Mod.sh")
        time.sleep(0.5)
        os.remove(des_dir + "/.modbranch")
        os.remove(src_dir + "/Mod.sh")
        return True


if __name__ == '__main__':
    Main(sys.argv[1], sys.argv[2], sys.argv[3])
