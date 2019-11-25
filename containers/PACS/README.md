# PACS-Stack
Maintainer: Matthias Greiner
Source: https://www.dcm4che.org/

### Deploy PACS Stack
```bash
cd PACS
docker-compose up -d

# Update hostname within the PACS-Config:

Web Service URLs
Archive UI: http://x.x.x.x:8080/dcm4chee-arc/ui2 - if secured, login with

Username - Password - Role
user - user - user
admin - admin - user + admin

Wildfly Administration Console: http://x.x.x.x:9990, login with Username: admin, Password: admin.

DICOM QIDO-RS Base URL: http://x.x.x.x:8090/dcm4chee-arc/aets/DCM4CHEE/rs
DICOM STOW-RS Base URL: http://x.x.x.x:8090/dcm4chee-arc/aets/DCM4CHEE/rs
DICOM WADO-RS Base URL: http://x.x.x.x:8090/dcm4chee-arc/aets/DCM4CHEE/rs
DICOM WADO-URI: http://x.x.x.x:8090/dcm4chee-arc/aets/DCM4CHEE/wado

IHE XDS-I Retrieve Imaging Document Set: http://x.x.x.x:8090/dcm4chee-arc/xdsi/ImagingDocumentSource
```
