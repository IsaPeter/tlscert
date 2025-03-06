import ssl
import socket
from argparse import ArgumentParser
from datetime import datetime


def parse_arguments():
  parser = ArgumentParser()
  parser.add_argument("-d","--domain", dest="domain", metavar="", help="Set target domain name [domain[:port]]")
  parser.add_argument("--san", dest="san", action="store_true", help="Collect Subject Alt Names")
  parser.add_argument("--san-list", dest="san_list", action="store_true", help="Collect Subject Alt Names and print each after")
  parser.add_argument("--dump", dest="dump", action="store_true", help="Dump Certificate data")
  parser.add_argument("--subject", dest="subject", action="store_true", help="Dump Certificate Subject") 
  parser.add_argument("--issuer", dest="issuer", action="store_true", help="Dump Certificate Issuer")
  parser.add_argument("--version", dest="version", action="store_true", help="Dump Certificate Version")
  parser.add_argument("--serial", dest="serial", action="store_true", help="Dump Certificate Serial Number")
  parser.add_argument("--not-before", dest="not_before", action="store_true", help="Dump Certificate Not Before Date")
  parser.add_argument("--not-after", dest="not_after", action="store_true", help="Dump Certificate Not After")




  return parser.parse_args()

def get_certificate(hostname, port):
  context = ssl.create_default_context()
  with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
      cert = ssock.getpeercert()
      return cert  


def main():
  args = parse_arguments()
 
  target_domain = ""
  target_port = 443

  if args.domain:
    if ":" in args.domain:
      target_domain, target_port = args.domain.split(":",1)
    else:
      target_domain = args.domain 

    certificate = get_certificate(target_domain, int(target_port))
    if certificate:
      if args.san:
        print("Subject Alt Names: ", ', '.join([item[1] for item in certificate["subjectAltName"]]))

      if args.san_list:
        for name in [item[1] for item in certificate["subjectAltName"]]:
          print(name)

      if args.subject:
        print("Subject (CN): ",certificate["subject"][0][0][1])

      if args.issuer:
        country_name = certificate["issuer"][0][0][1]
        org_name = certificate["issuer"][1][0][1]
        common_name = certificate["issuer"][2][0][1]

        print("Common Name: ", common_name)
        print("Organization Name: ", org_name)
        print("Country Name: ", country_name)

      if args.version:
        print("Version: ",certificate["version"])

      if args.serial:
        print("Serial Number: ",certificate["serialNumber"])

      if args.not_before:
        print("Not Before: ", certificate["notBefore"])

      if args.not_after:
        date_format = "%b %d %H:%M:%S %Y GMT"
        date_string = certificate["notAfter"]
        parsed_date = datetime.strptime(date_string, date_format)
        now = datetime.now()

        print("Not After: ", certificate["notAfter"], f"({(parsed_date-now).days} days left)")


      if args.dump:
        print(certificate)
      




if __name__ == '__main__':
  main()
