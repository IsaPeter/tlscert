# tlscert
TLS Certificate Grabber tool


## Usage

```bash
python3 tlscert.py -d medium.com --subject --issuer --version --serial --not-before --not-after --san           

Subject Alt Names:  medium.com, *.medium.com
Subject (CN):  medium.com
Common Name:  WE1
Organization Name:  Google Trust Services
Country Name:  US
Version:  3
Serial Number:  ACA3D500E0A554830EE773BBB35AFE78
Not Before:  Jan 23 18:19:36 2025 GMT
Not After:  Apr 23 19:19:35 2025 GMT
```

List available Subject Alt Names (SAN)

```bash
python3 tlscert.py -d medium.com --san-list                                                           
medium.com
*.medium.com             
```
