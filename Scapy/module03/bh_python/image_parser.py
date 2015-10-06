__author__ = 'root'

import re
import zlib
import cv2

from scapy.all import *

def get_http_headers(http_payload):
    try:
        # split headers off if it is HTTP traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]

        #break out headers
        headers = dict(re.findall(r"(?P<name>.*?):(?P<value>.*?)\r\n",headers_raw))

    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers

def extract_image(headers, http_payload):

    image = None
    image_type = None

    try:
        if "image" in headers['Content-Type']:
            #grab the image type and image body:
            image_type = headers['Content-Type'].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n")+4:]

            #if we detect compression decromress the image
            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image,16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except:
        return None, None

    return image, image_type


def http_assembler(pcap_file):
    carved_images = 0
    #faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        #print session
        #pause =raw_input("aa")
        http_payload = ""

        for packet in sessions[session]:

            try:
                if packet[TCP].dport == 80 or packet[TCP].sport ==80:
                    #
                    #reassemble the stream
                    http_payload += str(packet[TCP].payload)

                        #pause =raw_input("bb")
            except:
                #pause = raw_input("PASS")
                pass

        headers = get_http_headers(http_payload)

        if headers is None:

            #pause = raw_input("dd")
            continue
        #raw_input("cc")
        image, image_type = extract_image(headers,http_payload)
        #print len(image)



        if image is not None and image_type is not None:
            #pause = raw_input("bb")
            #store the image
            file_name = "%s-pic_carved_%d.%s" %(pcap_file,carved_images,image_type)

            fd = open("%s/%s" %(pictures_directory,file_name),"wb")

            fd.write(image)
            fd.close()

            carved_images +=1


            #now attempt face detection
            #not implemented yet


    return carved_images#, faces_detected


if __name__ == "__main__":
    pictures_directory = "/root/Desktop/pics"
    pcap_file = "arper.pcap"



#carved_images, faces_detected= http_assembler(pcap_file)
carved_images = http_assembler(pcap_file)
print "Extracted: %d Images" % carved_images
#print "Detected: %d faces" % faces_detected

